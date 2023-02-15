from django.db import models

# Create your models here.
class Doctor(models.Model):
    Name = models.CharField(max_length=50) 
    mobile = models.IntegerField()
    special = models.CharField(max_length=50)

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
    Nombre = models.CharField(max_length=100)
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
