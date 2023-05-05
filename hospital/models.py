from django.db import models

# Create your models here.
class Doctor(models.Model):
    Name = models.CharField(max_length=50) 
    mobile = models.IntegerField()
    special = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50,default='CCC-00000')

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    mobile = models.IntegerField(null=True)
    address = models.TextField()

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

class PacienteGenerales(models.Model):
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100,default='SinApellido',editable=True)
    Edad = models.IntegerField(null=True)
    Medico = models.CharField(max_length=100)
    Hospital = models.CharField(max_length=100)
    Muestra = models.CharField(max_length=200)
    Diagnostico = models.CharField(max_length=100)

class Muestra(models.Model):
    TomaDeMuestra = models.DateField(blank=True)
    Recepcion = models.DateField(blank=True)
    NumeroDeLaminas = models.IntegerField(blank=True)
    Tincion= models.CharField(max_length=100,blank=True)

class Informe(models.Model):
    PacienteInforme = models.ForeignKey(PacienteGenerales,on_delete=models.CASCADE)
    MuestraInforme = models.ForeignKey(Muestra,on_delete=models.CASCADE)

class CodigoInforme(models.Model):
    Codigo = models.CharField(max_length=20,default='000-X')

class EstudioMicroscopico(models.Model):
    DESCRIPCIONES = (
        ('OPT1', 'Extendido citológico convencional exo-endocervical'),
        ('OPT2', 'Extendido citológico post-histectomia'),
    )
    Descripcion = models.CharField(max_length=100,choices=DESCRIPCIONES)

class CalidadDeMuestra(models.Model):
    CALIDADES = (
        ('SAT1','Satisfactorio para valoración citológica: con presencia de células epiteliales de la zona de transformación'),
        ('INSAT1','Insatisfactorio por ausencia de células exocervicales'),
        ('INSAT2','Insatisfactorio por presencia de escasas células exocervicales'),
        ('INSAT3','Insatisfactorio por más del 75% de células cubiertas por hematies'),
        ('INSAT4','Insatisfactorio por más del 75% de células cubiertas por inflamación'),
        ('INSAT5','Insatisfactorio por más del 75% de células cubiertas por hematies e inflamación'),

    )
    Calidad = models.CharField(max_length=200, choices=CALIDADES)
class Microrganismos(models.Model):
    MICROS = (
        ('FLORA', 'Flora habitual'),
        ('FLORAB', 'Flora bacteriana mixta'),
        ('FLORAC', 'Flora cocoide'),
        ('CAMB', 'Cambios en la flora sugestivos de vaginosis bacteriana'),       
        ('TRICO', 'Trichonomas vaginalis'),
        ('ORG', 'Organismos micóticos morfologicamente compatibles con candida SP.'),
        ('BACT','Bacterias morfologicamente compatibles con Actynomices SP.'),
        ('CAMB2', 'Cambios compatibles con virus herpes simple'),
    )
    Microrgs = models.CharField(max_length=100, choices=MICROS)

class HallazgosNoNeoplasicos(models.Model):
    HALLAZGOS = (
        ('OPT1','Cambios celulares reactivos a la inflamación'),
        ('OPT2','Metaplasia escamosa'),
        ('OPT3','Metaplasia tubárica'),
        ('OPT4','Alteraciones atrófica'),
        ('OPT5','Alteraciones celulares secundarias a radioterapia'),
        ('OPT6','Alteraciones celulares secundarias a quimioterapia'),
        ('OPT7','Alteraciones celulares secundarias a DIUI'),
    )
    NoNeoplasicos = models.CharField(max_length=100, choices=HALLAZGOS)

class CelEscamosas(models.Model):
    ESCAMOSAS = (
        ('ASC-US', 'De significado indeterminado(ASC-US)'),
        ('ASC-H', 'No puede excluirse HSIL(ASC-H)'),
        ('L-SIL', 'Lesión intraepitelial escamosa de bajo grado(L-SIL)'),
        ('H-SIL', 'Lesión intraepitelial escamosa de alto grado(H-SIL)'),
        ('L-SIL2', 'Lesión intraepitelial escamosa de bajo grado(L-SIL) con cambios sugestivos de HPV'),
        ('CAR', 'Carcinoma epirdermoide')
    )
    Escamosas = models.CharField(max_length=100, choices=ESCAMOSAS)

class CelGlandulares(models.Model):
    GLANDULARES = (
        ('AT', 'Cel. gland. atipicas (CGA)'),
        ('AT2', 'Cel. gland. atipicas sugestivas de neoplasia'),
        ('AD', 'Adenocarcinoma'),
    )
    Glandulares = models.CharField(max_length=40, choices=GLANDULARES)

class EvaluacionHormonal(models.Model):
    EVAL = (
        ('PAT', 'Patron concordante con historia'),
        ('TROF', 'Trofico'),
        ('HIP', 'Hipotrofico'),
        ('ATRO', 'Atrofico'),
    )
    Evaluacion = models.CharField(max_length=20, choices=EVAL)

class Inflamacion (models.Model):
    INFL = (
        ('LEV', 'Leve'),
        ('MOD', 'Moderada'),
        ('SEV', 'Severa'),
        ('MOD2', 'Moderada-hemorragico'),
        ('MOD3', 'Severa-hemorragico'),
    )
    Inflamation = models.CharField(max_length=50, choices=INFL)

class Conclusion(models.Model):
    CONCLU = (
        ('CONCL1','Negativo para lesión intraepitelial o malignidad'),
        ('CONCL2','Anomalía de células epiteliales'),
        ('CONCL3','Positivo para lesión intraepitelial'),
        ('CONCL4','Positivo para neoplasia maligna'),
    )
    Conclusion = models.CharField(max_length=100,choices=CONCLU)

class Recomendacion(models.Model):
    Recomendacion = models.CharField(max_length=1000,default='Sin descripcion')

class FechaPie(models.Model):
    Fecha = models.DateField(blank=True)

class Lugar(models.Model):
    LUGARES = (
        ('LP', 'La Paz'),
        ('EA', 'El Alto'),
    )
    Lugar = models.CharField(max_length=20, choices=LUGARES)

class InformeCito(models.Model):
    CodigoInformeCito = models.ForeignKey(CodigoInforme,on_delete=models.CASCADE)
    PacienteInformeCito = models.ForeignKey(PacienteGenerales,on_delete=models.CASCADE)
    MuestraInformeCito = models.ForeignKey(Muestra,on_delete=models.CASCADE)
    EstudioMicroscopicoInformeCito = models.ForeignKey(EstudioMicroscopico,on_delete=models.CASCADE)
    CalidadDeMuestraInformeCito = models.ForeignKey(CalidadDeMuestra,on_delete=models.CASCADE)
    MicrorganismosInformeCito = models.ForeignKey(Microrganismos,on_delete=models.CASCADE)
    HallazgosInformeCito = models.ForeignKey(HallazgosNoNeoplasicos,on_delete=models.CASCADE)
    CelEscamosasInformeCito = models.ForeignKey(CelEscamosas,on_delete=models.CASCADE)
    CelGlandularesInformeCito = models.ForeignKey(CelGlandulares,on_delete=models.CASCADE)
    EvaluacionHormonalInformeCito = models.ForeignKey(EvaluacionHormonal,on_delete=models.CASCADE)
    InflamacionInformeCito = models.ForeignKey(Inflamacion,on_delete=models.CASCADE)
    ConclusionInformeCito = models.ForeignKey(Conclusion,on_delete=models.CASCADE)
    RecomendacionInformeCito = models.ForeignKey(Recomendacion,on_delete=models.CASCADE)
    FechaPieInformeCito = models.ForeignKey(FechaPie,on_delete=models.CASCADE)
    LugarInformeCito = models.ForeignKey(Lugar,on_delete=models.CASCADE)
    DoctorInformeCito = models.ForeignKey(Doctor,on_delete=models.CASCADE)

class InformeAnato(models.Model):
    CodigoInformeAnato = models.ForeignKey(CodigoInforme,on_delete=models.CASCADE)
    PacienteInformeAnato = models.ForeignKey(PacienteGenerales,on_delete=models.CASCADE)
    MuestraInformeAnato = models.ForeignKey(Muestra,on_delete=models.CASCADE)
    EstudioMacroscopicoInformeAnato =  models.CharField(max_length=1000,default='Sin descripcion')
    EstudioMicroscopicoInformeAnato =  models.CharField(max_length=1000,default='Sin descripcion')
    EspecimenInformeAnato = models.CharField(max_length=200,default='Sin descripcion')
    ConclusionInformeAnato = models.CharField(max_length=200,default='Sin descripcion')
    FechaPieInformeAnato = models.ForeignKey(FechaPie,on_delete=models.CASCADE)
    LugarInformeAnato = models.ForeignKey(Lugar,on_delete=models.CASCADE)
    DoctorInformeAnato = models.ForeignKey(Doctor,on_delete=models.CASCADE)

class InformeCito2(models.Model):
    CodigoInformeCito2 = models.ForeignKey(CodigoInforme,on_delete=models.CASCADE)
    PacienteInformeCito2 = models.ForeignKey(PacienteGenerales,on_delete=models.CASCADE)
    MuestraInformeCito2 = models.ForeignKey(Muestra,on_delete=models.CASCADE)
    EstudioMicroscopicoInformeCito2 = models.CharField(max_length=200,default='Sin descripcion')
    CalidadDeMuestraInformeCito2 = models.CharField(max_length=200,default='Sin descripcion')
    MicrorganismosInformeCito2 = models.CharField(max_length=200,default='Sin descripcion')
    HallazgosInformeCito2 = models.CharField(max_length=200,default='Sin descripcion')
    CelEscamosasInformeCito2 = models.CharField(max_length=200,default='Sin descripcion')
    CelGlandularesInformeCito2 = models.CharField(max_length=100,default='Sin descripcion')
    EvaluacionHormonalInformeCito2 = models.CharField(max_length=100,default='Sin descripcion') 
    InflamacionInformeCito2 = models.CharField(max_length=100,default='Sin descripcion')
    ConclusionInformeCito2 = models.CharField(max_length=200,default='Sin descripcion')
    OpcionalInformeCito2 = models.CharField(max_length=100,default='Sin descripcion')
    RecomendacionInformeCito2 = models.CharField(max_length=1000,default='Sin descripcion')
    FechaPieInformeAnato2 = models.ForeignKey(FechaPie,on_delete=models.CASCADE)
    LugarInformeAnato2 = models.ForeignKey(Lugar,on_delete=models.CASCADE)
    DoctorInformeAnato2 = models.ForeignKey(Doctor,on_delete=models.CASCADE)
