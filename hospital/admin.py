from django.contrib import admin
from.models import Patient, Doctor, Appointment,PacienteGenerales,Muestra,Informe
from.models import EstudioMicroscopico,CalidadDeMuestra, Microrganismos, CelEscamosas, CelGlandulares
from.models import EvaluacionHormonal, Inflamacion, Conclusion, Recomendacion, FechaPie, Lugar, InformeCito
from.models import CodigoInforme, HallazgosNoNeoplasicos
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(PacienteGenerales)
admin.site.register(Muestra)
admin.site.register(Informe)
admin.site.register(CodigoInforme)
admin.site.register(EstudioMicroscopico)
admin.site.register(CalidadDeMuestra)
admin.site.register(Microrganismos)
admin.site.register(HallazgosNoNeoplasicos)
admin.site.register(CelEscamosas)
admin.site.register(CelGlandulares)
admin.site.register(EvaluacionHormonal)
admin.site.register(Inflamacion)
admin.site.register(Conclusion)
admin.site.register(Recomendacion)
admin.site.register(FechaPie)
admin.site.register(Lugar)
admin.site.register(InformeCito)



