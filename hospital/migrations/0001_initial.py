# Generated by Django 4.1.7 on 2023-05-27 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('mobile', models.IntegerField()),
                ('special', models.CharField(max_length=50)),
                ('matricula', models.CharField(default='CCC-00000', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InformeCitologico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodigoInformeCitologico', models.CharField(max_length=20)),
                ('NombresInformeCitologico', models.CharField(max_length=100)),
                ('ApellidosInformeCitologico', models.CharField(max_length=100)),
                ('EdadInformeCitologico', models.IntegerField(null=True)),
                ('MedicoInformeCitologico', models.CharField(max_length=100)),
                ('HospitalInformeCitologico', models.CharField(max_length=100)),
                ('MuestraInformeCitologico', models.CharField(max_length=200)),
                ('DiagnosticoInformeCitologico', models.CharField(max_length=100)),
                ('TomaDeMuestraInformeCitologico', models.DateField(blank=True)),
                ('RecepcionInformeCitologico', models.DateField(blank=True)),
                ('NumeroDeLaminasInformeCitologico', models.IntegerField(blank=True)),
                ('TincionInformeCitologico', models.CharField(blank=True, max_length=100)),
                ('EstudioMicroscopicoInformeCitologico', models.CharField(default='Sin descripcion', max_length=200)),
                ('CalidadDeMuestraInformeCitologico', models.CharField(default='Sin descripcion', max_length=200)),
                ('MicrorganismosInformeCitologico', models.CharField(default='Sin descripcion', max_length=200)),
                ('HallazgosInformeCitologico', models.CharField(default='Sin descripcion', max_length=200)),
                ('CelEscamosasInformeCitologico', models.CharField(default='Sin descripcion', max_length=200)),
                ('CelGlandularesInformeCitologico', models.CharField(default='Sin descripcion', max_length=100)),
                ('EvaluacionHormonalInformeCitologico', models.CharField(default='Sin descripcion', max_length=100)),
                ('InflamacionInformeCitologico', models.CharField(default='Sin descripcion', max_length=100)),
                ('ConclusionInformeCitologico', models.CharField(default='Sin descripcion', max_length=200)),
                ('OpcionalInformeCitologico', models.CharField(default='Sin descripcion', max_length=100)),
                ('RecomendacionInformeCitologico', models.CharField(default='Sin descripcion', max_length=1000)),
                ('FechaPieInformeCitologico', models.DateField(blank=True)),
                ('LugarInformeCitologico', models.CharField(max_length=100)),
                ('DoctorInformeCitologico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='InformeAnatomico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodigoInformeAnatomico', models.CharField(max_length=20)),
                ('NombresInformeAnatomico', models.CharField(max_length=100)),
                ('ApellidosInformeAnatomico', models.CharField(max_length=100)),
                ('EdadInformeAnatomico', models.IntegerField(null=True)),
                ('MedicoInformeAnatomico', models.CharField(max_length=100)),
                ('HospitalInformeAnatomico', models.CharField(max_length=100)),
                ('MuestraInformeAnatomico', models.CharField(max_length=200)),
                ('DiagnosticoInformeAnatomico', models.CharField(max_length=100)),
                ('RecepcionInformeAnatomico', models.DateField(blank=True)),
                ('EstudioMacroscopicoInformeAnatomico', models.CharField(default='Sin descripcion', max_length=1000)),
                ('EstudioMicroscopicoInformeAnatomico', models.CharField(default='Sin descripcion', max_length=1000)),
                ('EspecimenInformeAnatomico', models.CharField(default='Sin descripcion', max_length=200)),
                ('ConclusionInformeAnatomico', models.CharField(default='Sin descripcion', max_length=200)),
                ('FechaPieInformeAnatomico', models.DateField(blank=True)),
                ('LugarInformeAnatomico', models.CharField(max_length=100)),
                ('DoctorInformeAnatomico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.doctor')),
            ],
        ),
    ]
