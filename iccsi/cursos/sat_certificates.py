import os
import base64
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

class SATCertificateService:
    """
    Servicio para manejar certificados SAT (.cer y .key)
    Permite firmar digitalmente XMLs CFDI 4.0
    """
    
    def __init__(self, certificate_path=None, key_path=None, password=None):
        self.certificate_path = certificate_path
        self.key_path = key_path
        self.password = password
        self.certificate = None
        self.private_key = None
        
    def load_certificate(self, certificate_path):
        """Carga el certificado .cer del SAT"""
        try:
            with open(certificate_path, 'rb') as cert_file:
                self.certificate = x509.load_der_x509_certificate(
                    cert_file.read(), 
                    default_backend()
                )
            self.certificate_path = certificate_path
            logger.info(f"Certificado cargado exitosamente: {certificate_path}")
            return True
        except Exception as e:
            logger.error(f"Error al cargar certificado: {e}")
            return False
    
    def load_private_key(self, key_path, password=None):
        """Carga la clave privada .key del SAT"""
        try:
            with open(key_path, 'rb') as key_file:
                if password:
                    self.private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=password.encode('utf-8'),
                        backend=default_backend()
                    )
                else:
                    self.private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=None,
                        backend=default_backend()
                    )
            self.key_path = key_path
            self.password = password
            logger.info(f"Clave privada cargada exitosamente: {key_path}")
            return True
        except Exception as e:
            logger.error(f"Error al cargar clave privada: {e}")
            return False
    
    def get_certificate_number(self):
        """Obtiene el número de certificado del SAT"""
        if self.certificate:
            return self.certificate.serial_number
        return None
    
    def get_certificate_expiry(self):
        """Obtiene la fecha de expiración del certificado"""
        if self.certificate:
            return self.certificate.not_valid_after
        return None
    
    def is_certificate_valid(self):
        """Verifica si el certificado está vigente"""
        if self.certificate:
            from datetime import datetime
            now = datetime.now()
            return (self.certificate.not_valid_before <= now <= self.certificate.not_valid_after)
        return False
    
    def sign_data(self, data_to_sign):
        """
        Firma digitalmente los datos usando el certificado SAT
        Retorna la firma en base64
        """
        if not self.private_key:
            raise ValueError("Clave privada no cargada")
        
        try:
            # Crear hash SHA256 de los datos
            hash_algorithm = hashes.SHA256()
            hasher = hashlib.sha256()
            hasher.update(data_to_sign.encode('utf-8'))
            data_hash = hasher.digest()
            
            # Firmar con la clave privada
            signature = self.private_key.sign(
                data_hash,
                padding.PKCS1v15(),
                hash_algorithm
            )
            
            # Convertir a base64
            signature_b64 = base64.b64encode(signature).decode('utf-8')
            logger.info("Datos firmados exitosamente")
            return signature_b64
            
        except Exception as e:
            logger.error(f"Error al firmar datos: {e}")
            raise
    
    def generate_original_string(self, cfdi_data):
        """
        Genera la cadena original del CFDI según especificaciones del SAT
        """
        try:
            # Ordenar elementos según especificación SAT
            ordered_elements = [
                f"||{cfdi_data.get('version', '4.0')}",
                f"|{cfdi_data.get('fecha', '')}",
                f"|{cfdi_data.get('forma_pago', '')}",
                f"|{cfdi_data.get('subtotal', '0.00')}",
                f"|{cfdi_data.get('moneda', 'MXN')}",
                f"|{cfdi_data.get('tipo_cambio', '1')}",
                f"|{cfdi_data.get('total', '0.00')}",
                f"|{cfdi_data.get('tipo_comprobante', 'I')}",
                f"|{cfdi_data.get('metodo_pago', 'PUE')}",
                f"|{cfdi_data.get('lugar_expedicion', '')}",
                f"|{cfdi_data.get('confirmacion', '')}",
            ]
            
            # Agregar datos del emisor
            emisor = cfdi_data.get('emisor', {})
            ordered_elements.extend([
                f"|{emisor.get('rfc', '')}",
                f"|{emisor.get('nombre', '')}",
                f"|{emisor.get('regimen_fiscal', '')}",
            ])
            
            # Agregar datos del receptor
            receptor = cfdi_data.get('receptor', {})
            ordered_elements.extend([
                f"|{receptor.get('rfc', '')}",
                f"|{receptor.get('nombre', '')}",
                f"|{receptor.get('uso_cfdi', '')}",
            ])
            
            # Agregar conceptos
            conceptos = cfdi_data.get('conceptos', [])
            for concepto in conceptos:
                ordered_elements.extend([
                    f"|{concepto.get('cantidad', '')}",
                    f"|{concepto.get('unidad', '')}",
                    f"|{concepto.get('descripcion', '')}",
                    f"|{concepto.get('valor_unitario', '')}",
                    f"|{concepto.get('importe', '')}",
                ])
            
            # Agregar impuestos
            impuestos = cfdi_data.get('impuestos', {})
            if impuestos:
                traslados = impuestos.get('traslados', [])
                for traslado in traslados:
                    ordered_elements.extend([
                        f"|{traslado.get('impuesto', '')}",
                        f"|{traslado.get('tipo_factor', '')}",
                        f"|{traslado.get('tasa_cuota', '')}",
                        f"|{traslado.get('importe', '')}",
                    ])
            
            # Construir cadena original
            original_string = ''.join(ordered_elements) + "||"
            
            logger.info("Cadena original generada exitosamente")
            return original_string
            
        except Exception as e:
            logger.error(f"Error al generar cadena original: {e}")
            raise
    
    def sign_cfdi(self, cfdi_data):
        """
        Firma un CFDI completo
        Retorna: (cadena_original, sello_digital)
        """
        try:
            # Generar cadena original
            original_string = self.generate_original_string(cfdi_data)
            
            # Firmar la cadena original
            sello_digital = self.sign_data(original_string)
            
            return original_string, sello_digital
            
        except Exception as e:
            logger.error(f"Error al firmar CFDI: {e}")
            raise
    
    def verify_signature(self, data, signature):
        """
        Verifica una firma digital
        """
        if not self.certificate:
            raise ValueError("Certificado no cargado")
        
        try:
            # Decodificar firma de base64
            signature_bytes = base64.b64decode(signature)
            
            # Crear hash de los datos
            hasher = hashlib.sha256()
            hasher.update(data.encode('utf-8'))
            data_hash = hasher.digest()
            
            # Verificar firma con clave pública
            public_key = self.certificate.public_key()
            public_key.verify(
                signature_bytes,
                data_hash,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            
            logger.info("Firma verificada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al verificar firma: {e}")
            return False
    
    def save_certificate_files(self, cer_file, key_file, password=None):
        """
        Guarda los archivos de certificado de forma segura
        """
        try:
            # Crear directorio para certificados si no existe
            cert_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
            os.makedirs(cert_dir, exist_ok=True)
            
            # Guardar archivo .cer
            cer_path = os.path.join(cert_dir, 'sat_certificate.cer')
            with default_storage.open(cer_path, 'wb') as f:
                f.write(cer_file.read())
            
            # Guardar archivo .key
            key_path = os.path.join(cert_dir, 'sat_private_key.key')
            with default_storage.open(key_path, 'wb') as f:
                f.write(key_file.read())
            
            # Cargar certificados
            self.load_certificate(cer_path)
            self.load_private_key(key_path, password)
            
            logger.info("Certificados guardados y cargados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar certificados: {e}")
            return False


class CertificateManager:
    """
    Gestor de certificados para múltiples emisores
    """
    
    def __init__(self):
        self.certificates = {}
    
    def add_certificate(self, emisor_rfc, certificate_path, key_path, password=None):
        """Agrega un certificado para un emisor específico"""
        try:
            service = SATCertificateService()
            if service.load_certificate(certificate_path) and service.load_private_key(key_path, password):
                self.certificates[emisor_rfc] = service
                logger.info(f"Certificado agregado para emisor: {emisor_rfc}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al agregar certificado: {e}")
            return False
    
    def get_certificate(self, emisor_rfc):
        """Obtiene el certificado de un emisor específico"""
        return self.certificates.get(emisor_rfc)
    
    def sign_cfdi_for_emisor(self, emisor_rfc, cfdi_data):
        """Firma un CFDI para un emisor específico"""
        service = self.get_certificate(emisor_rfc)
        if service:
            return service.sign_cfdi(cfdi_data)
        else:
            raise ValueError(f"No se encontró certificado para el emisor: {emisor_rfc}")
    
    def list_emisores(self):
        """Lista todos los emisores con certificados"""
        return list(self.certificates.keys())


# Instancia global del gestor de certificados
certificate_manager = CertificateManager()
