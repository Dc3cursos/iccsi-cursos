from django import forms
from .models import Curso, Empresa, Pago

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'duracion_horas', 'organizacion', 'imagen', 'video']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del curso'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del curso'
            }),
            'duracion_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Horas de duración'
            }),
            'organizacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            })
        }

class DC3GenerateForm(forms.Form):
    # Información del trabajador
    apellido_paterno = forms.CharField(
        max_length=100, 
        label='Apellido paterno', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: GARCÍA'
        })
    )
    apellido_materno = forms.CharField(
        max_length=100, 
        label='Apellido materno', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: LÓPEZ'
        })
    )
    nombres = forms.CharField(
        max_length=200, 
        label='Nombre(s)', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: JUAN CARLOS'
        })
    )
    curp = forms.CharField(
        max_length=18, 
        label='CURP', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: GALJ800101HDFXXX01'
        })
    )
    puesto = forms.CharField(
        max_length=100, 
        label='Puesto o cargo', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: OPERADOR DE MAQUINARIA'
        })
    )


    # Información del curso
    nombre_curso = forms.CharField(
        max_length=255, 
        label='Nombre del curso', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: PREVENCIÓN DE RIESGOS LABORALES'
        })
    )
    horas_curso = forms.ChoiceField(
        choices=[],  # Se llenará dinámicamente en __init__
        label='Horas del curso', 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Información de la empresa
    nombre_empresa = forms.CharField(
        max_length=200, 
        label='Nombre de la empresa', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: EMPRESA INDUSTRIAL S.A. DE C.V.'
        })
    )
    rfc_empresa = forms.CharField(
        max_length=13, 
        label='RFC de la empresa', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: EIN123456789'
        })
    )
    representante_legal = forms.CharField(
        max_length=200, 
        label='Nombre del representante legal', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: LIC. MARÍA GONZÁLEZ PÉREZ'
        })
    )
    representante_trabajadores = forms.CharField(
        max_length=200, 
        label='Nombre del representante de los trabajadores', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: ING. CARLOS RODRÍGUEZ MARTÍNEZ'
        })
    )

    # Fechas del curso
    fecha_inicio = forms.DateField(
        label='Fecha de inicio del curso',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_fin = forms.DateField(
        label='Fecha de fin del curso',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    # Información del instructor
    instructor_nombre = forms.CharField(
        max_length=200, 
        label='Nombre del instructor', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: MTRO. ROBERTO SÁNCHEZ DÍAZ'
        })
    )

    # Selección de plantilla
    plantilla = forms.ChoiceField(
        choices=[],
        label='Plantilla de certificado',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar plantillas dinámicamente desde la base de datos
        from .models import PlantillaDC3
        plantillas = PlantillaDC3.objects.filter(activo=True).order_by('nombre')
        choices = [(plantilla.id, f"{plantilla.nombre} ({plantilla.organizacion.nombre if plantilla.organizacion else 'General'})") 
                  for plantilla in plantillas]
        self.fields['plantilla'].choices = choices
        
        # Cargar horas de cursos dinámicamente desde la base de datos
        from .models import Curso
        horas_unicas = Curso.objects.exclude(
            duracion_horas__isnull=True
        ).values_list('duracion_horas', flat=True).distinct().order_by('duracion_horas')
        
        horas_choices = [(str(horas), f'{horas} horas') for horas in horas_unicas]
        self.fields['horas_curso'].choices = horas_choices
        
        # Convertir a mayúsculas automáticamente
        for field_name in self.fields:
            if isinstance(self.fields[field_name].widget, forms.TextInput):
                self.fields[field_name].widget.attrs['style'] = 'text-transform: uppercase;'
                self.fields[field_name].widget.attrs['oninput'] = 'this.value = this.value.toUpperCase();'

    def clean(self):
        cleaned_data = super().clean()
        # Convertir todo a mayúsculas
        for field_name in self.fields:
            val = cleaned_data.get(field_name)
            if isinstance(val, str):
                cleaned_data[field_name] = val.upper().strip()
        return cleaned_data


class PagoForm(forms.ModelForm):
    """Formulario para procesar pagos"""
    class Meta:
        model = Pago
        fields = ['metodo_pago']
        widgets = {
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select',
                'id': 'metodo_pago'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['metodo_pago'].label = 'Método de Pago'
        self.fields['metodo_pago'].help_text = 'Selecciona tu método de pago preferido'