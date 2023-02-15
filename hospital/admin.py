from django.contrib import admin
from.models import Patient, Doctor, Appointment,PacienteGenerales,Muestra,Informe

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(PacienteGenerales)
admin.site.register(Muestra)
admin.site.register(Informe)


