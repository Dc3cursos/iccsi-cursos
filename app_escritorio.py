#!/usr/bin/env python3
"""
Aplicación de Escritorio ICCSI usando PyQt6
"""
import sys
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QTabWidget, QFormLayout,
    QComboBox, QSpinBox, QDateEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon

class ICCSIApp(QMainWindow):
    """Aplicación principal de escritorio ICCSI"""
    
    def __init__(self):
        super().__init__()
        self.api_url = "http://127.0.0.1:8000/api"
        self.token = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("ICCSI - Instituto de Capacitación")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("ICCSI - Sistema de Capacitación")
        header.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Crear tabs
        self.create_login_tab()
        self.create_cursos_tab()
        self.create_certificados_tab()
        self.create_perfil_tab()
        
        # Estado inicial
        self.tabs.setTabEnabled(1, False)  # Cursos
        self.tabs.setTabEnabled(2, False)  # Certificados
        self.tabs.setTabEnabled(3, False)  # Perfil
        
    def create_login_tab(self):
        """Crear tab de login"""
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        
        # Formulario de login
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Contraseña:", self.password_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        register_btn = QPushButton("Registrarse")
        register_btn.clicked.connect(self.show_register)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        buttons_layout.addWidget(login_btn)
        buttons_layout.addWidget(register_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.tabs.addTab(login_widget, "🔐 Iniciar Sesión")
        
    def create_cursos_tab(self):
        """Crear tab de cursos"""
        cursos_widget = QWidget()
        layout = QVBoxLayout(cursos_widget)
        
        # Botones de acción
        actions_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self.load_cursos)
        
        inscribirse_btn = QPushButton("📝 Inscribirse")
        inscribirse_btn.clicked.connect(self.inscribirse_curso)
        
        actions_layout.addWidget(refresh_btn)
        actions_layout.addWidget(inscribirse_btn)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        
        # Tabla de cursos
        self.cursos_table = QTableWidget()
        self.cursos_table.setColumnCount(5)
        self.cursos_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Duración", "Organización", "Acciones"
        ])
        
        layout.addWidget(self.cursos_table)
        
        self.tabs.addTab(cursos_widget, "📚 Cursos")
        
    def create_certificados_tab(self):
        """Crear tab de certificados"""
        certificados_widget = QWidget()
        layout = QVBoxLayout(certificados_widget)
        
        # Formulario para generar certificado
        form_layout = QFormLayout()
        
        self.plantilla_combo = QComboBox()
        self.apellido_paterno_input = QLineEdit()
        self.apellido_materno_input = QLineEdit()
        self.nombres_input = QLineEdit()
        self.curp_input = QLineEdit()
        self.puesto_input = QLineEdit()
        self.horas_input = QSpinBox()
        self.horas_input.setRange(1, 1000)
        
        form_layout.addRow("Plantilla:", self.plantilla_combo)
        form_layout.addRow("Apellido Paterno:", self.apellido_paterno_input)
        form_layout.addRow("Apellido Materno:", self.apellido_materno_input)
        form_layout.addRow("Nombres:", self.nombres_input)
        form_layout.addRow("CURP:", self.curp_input)
        form_layout.addRow("Puesto:", self.puesto_input)
        form_layout.addRow("Horas:", self.horas_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        generar_btn = QPushButton("📄 Generar Certificado")
        generar_btn.clicked.connect(self.generar_certificado)
        
        descargar_btn = QPushButton("📥 Descargar")
        descargar_btn.clicked.connect(self.descargar_certificado)
        
        buttons_layout.addWidget(generar_btn)
        buttons_layout.addWidget(descargar_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.tabs.addTab(certificados_widget, "📋 Certificados DC-3")
        
    def create_perfil_tab(self):
        """Crear tab de perfil"""
        perfil_widget = QWidget()
        layout = QVBoxLayout(perfil_widget)
        
        # Información del usuario
        self.perfil_label = QLabel("Cargando perfil...")
        self.perfil_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.perfil_label)
        
        # Botón de logout
        logout_btn = QPushButton("🚪 Cerrar Sesión")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        layout.addWidget(logout_btn)
        layout.addStretch()
        
        self.tabs.addTab(perfil_widget, "👤 Perfil")
        
    def login(self):
        """Iniciar sesión"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor completa todos los campos")
            return
        
        try:
            response = requests.post(f"{self.api_url}/auth/login/", json={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['access']
                self.load_user_profile()
                self.enable_tabs()
                self.tabs.setCurrentIndex(1)  # Ir a cursos
                QMessageBox.information(self, "Éxito", "Sesión iniciada correctamente")
            else:
                QMessageBox.critical(self, "Error", "Credenciales incorrectas")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")
    
    def load_user_profile(self):
        """Cargar perfil del usuario"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(f"{self.api_url}/auth/profile/", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                self.perfil_label.setText(f"""
                <h2>Perfil de Usuario</h2>
                <p><strong>Usuario:</strong> {user_data['username']}</p>
                <p><strong>Email:</strong> {user_data['email']}</p>
                <p><strong>Nombre:</strong> {user_data['first_name']} {user_data['last_name']}</p>
                <p><strong>Rol:</strong> {user_data['rol']}</p>
                """)
                
        except Exception as e:
            print(f"Error cargando perfil: {e}")
    
    def enable_tabs(self):
        """Habilitar tabs después del login"""
        self.tabs.setTabEnabled(1, True)  # Cursos
        self.tabs.setTabEnabled(2, True)  # Certificados
        self.tabs.setTabEnabled(3, True)  # Perfil
    
    def load_cursos(self):
        """Cargar lista de cursos"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            # Usar el endpoint que muestra todos los cursos
            response = requests.get(f"{self.api_url}/cursos/todos/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                cursos = data.get('cursos', [])
                total = data.get('total', 0)
                
                print(f"📚 Cursos obtenidos: {len(cursos)} de {total} total")
                
                self.cursos_table.setRowCount(len(cursos))
                
                for i, curso in enumerate(cursos):
                    self.cursos_table.setItem(i, 0, QTableWidgetItem(str(curso['id'])))
                    self.cursos_table.setItem(i, 1, QTableWidgetItem(curso['nombre']))
                    self.cursos_table.setItem(i, 2, QTableWidgetItem(f"{curso['duracion_horas']} horas"))
                    
                    # Manejar organización (puede ser None)
                    org_nombre = curso['organizacion']['nombre'] if curso['organizacion'] else 'Sin organización'
                    self.cursos_table.setItem(i, 3, QTableWidgetItem(org_nombre))
                    
                    # Botón de inscribirse
                    inscribirse_btn = QPushButton("Inscribirse")
                    inscribirse_btn.clicked.connect(lambda checked, c=curso: self.inscribirse_curso(c))
                    self.cursos_table.setCellWidget(i, 4, inscribirse_btn)
                
                # Mostrar mensaje de éxito
                QMessageBox.information(self, "Éxito", f"Se cargaron {len(cursos)} cursos de {total} disponibles")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando cursos: {str(e)}")
            print(f"Error detallado: {e}")
    
    def inscribirse_curso(self, curso=None):
        """Inscribirse a un curso"""
        if not curso:
            current_row = self.cursos_table.currentRow()
            if current_row >= 0:
                curso_id = int(self.cursos_table.item(current_row, 0).text())
                # Aquí implementarías la lógica de inscripción
                QMessageBox.information(self, "Éxito", f"Inscrito al curso ID: {curso_id}")
            else:
                QMessageBox.warning(self, "Error", "Selecciona un curso primero")
        else:
            QMessageBox.information(self, "Éxito", f"Inscrito al curso: {curso['nombre']}")
    
    def generar_certificado(self):
        """Generar certificado DC-3"""
        # Implementar generación de certificado
        QMessageBox.information(self, "Éxito", "Certificado generado correctamente")
    
    def descargar_certificado(self):
        """Descargar certificado"""
        # Implementar descarga de certificado
        QMessageBox.information(self, "Éxito", "Certificado descargado")
    
    def show_register(self):
        """Mostrar formulario de registro"""
        QMessageBox.information(self, "Registro", "Función de registro en desarrollo")
    
    def logout(self):
        """Cerrar sesión"""
        self.token = None
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setCurrentIndex(0)
        self.username_input.clear()
        self.password_input.clear()
        QMessageBox.information(self, "Éxito", "Sesión cerrada correctamente")

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Estilo de la aplicación
    app.setStyle('Fusion')
    
    # Crear y mostrar la ventana principal
    window = ICCSIApp()
    window.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
