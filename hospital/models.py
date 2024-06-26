from django.db import models

# Create your models here.
class Doctor(models.Model):
    Name = models.CharField(max_length=50) 
    mobile = models.IntegerField()
    special = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50,default='CCC-00000')



class InformeCitologico(models.Model):
    
    
    CodigoInformeCitologico = models.CharField(max_length=20)
    
    NombresInformeCitologico = models.CharField(max_length=100)
    ApellidosInformeCitologico = models.CharField(max_length=100)
    EdadInformeCitologico = models.IntegerField(null=True)
    MedicoInformeCitologico = models.CharField(max_length=100)
    HospitalInformeCitologico = models.CharField(max_length=100)
    MuestraInformeCitologico = models.CharField(max_length=200)
    DiagnosticoInformeCitologico = models.CharField(max_length=100)
    
    TomaDeMuestraInformeCitologico = models.DateField(blank=True)
    RecepcionInformeCitologico = models.DateField(blank=True)
    NumeroDeLaminasInformeCitologico = models.IntegerField(blank=True)
    TincionInformeCitologico= models.CharField(max_length=100,blank=True)
    
    EstudioMicroscopicoInformeCitologico = models.CharField(max_length=200,default='Sin descripcion')
    CalidadDeMuestraInformeCitologico = models.CharField(max_length=200,default='Sin descripcion')
    MicrorganismosInformeCitologico = models.CharField(max_length=200,default='Sin descripcion')
    HallazgosInformeCitologico = models.CharField(max_length=200,default='Sin descripcion')
    CelEscamosasInformeCitologico = models.CharField(max_length=200,default='Sin descripcion')
    CelGlandularesInformeCitologico = models.CharField(max_length=100,default='Sin descripcion')
    EvaluacionHormonalInformeCitologico = models.CharField(max_length=100,default='Sin descripcion') 
    InflamacionInformeCitologico = models.CharField(max_length=100,default='Sin descripcion')
    ConclusionInformeCitologico = models.CharField(max_length=200,default='Sin descripcion')
    OpcionalInformeCitologico = models.CharField(max_length=100,default='Sin descripcion')
    RecomendacionInformeCitologico = models.CharField(max_length=1000,default='Sin descripcion')
    
    FechaPieInformeCitologico = models.DateField(blank=True)
    
    LugarInformeCitologico = models.CharField(max_length=100)
    DoctorInformeCitologico = models.ForeignKey(Doctor,on_delete=models.CASCADE)

class InformeAnatomico(models.Model):
    
    CodigoInformeAnatomico = models.CharField(max_length=20)
    
    NombresInformeAnatomico = models.CharField(max_length=100)
    ApellidosInformeAnatomico = models.CharField(max_length=100)
    EdadInformeAnatomico = models.IntegerField(null=True)
    MedicoInformeAnatomico = models.CharField(max_length=100)
    HospitalInformeAnatomico = models.CharField(max_length=100)
    MuestraInformeAnatomico = models.CharField(max_length=200)
    DiagnosticoInformeAnatomico = models.CharField(max_length=100)
    
    RecepcionInformeAnatomico = models.DateField(blank=True)
    
    
    EstudioMacroscopicoInformeAnatomico =  models.CharField(max_length=1000,default='Sin descripcion')
    EstudioMicroscopicoInformeAnatomico =  models.CharField(max_length=1000,default='Sin descripcion')
    EspecimenInformeAnatomico = models.CharField(max_length=200,default='Sin descripcion')
    ConclusionInformeAnatomico = models.CharField(max_length=200,default='Sin descripcion')
    FechaPieInformeAnatomico = models.DateField(blank=True)
    LugarInformeAnatomico = models.CharField(max_length=100)
    
    DoctorInformeAnatomico = models.ForeignKey(Doctor,on_delete=models.CASCADE)

    
