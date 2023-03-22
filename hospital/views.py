from django.shortcuts import render, redirect
# from django.fpdf2 import FPDF
# import io
# from django.http import FileResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Paragraph, Table
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import utils
from reportlab.lib import colors
from datetime import datetime, date
import locale



from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Doctor,Patient,Appointment,PacienteGenerales,Muestra, Informe

from .models import CodigoInforme, CalidadDeMuestra, EstudioMicroscopico, Microrganismos, CelEscamosas, CelGlandulares
from .models import HallazgosNoNeoplasicos, EvaluacionHormonal, Inflamacion, Conclusion, Recomendacion, FechaPie, Lugar, InformeCito

import logging
# from django.http import HttpResponse

# Create your views here.

def About(request):
    # return HttpResponse("<h1>this is the about section</h1>")
    return render (request,'about.html') 

def Home(request):
    return render (request,'home.html')

def Contact(request):
    return render (request,'contact.html')

def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.all()
    patient = Patient.objects.all()
    appointment = Appointment.objects.all()
    d=0
    p=0
    a=0
    for i in doctors:
        d+=1
    
    for i in patient:
        p+=1

    for i in appointment:
        a+=1
    
    d1={'d':d,'p':p,'a':a}

    return render(request,'index.html',d1)

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username = u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error = "yes"
        except:
            error ="yes"
    d = {'error':error}
    return render(request, 'login.html', d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    logout(request)
    return redirect('admin_login')

def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'view_doctor.html',d)

def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def Add_Doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST['name']
        m = request.POST['mobile']
        sp = request.POST['special']
        mat = request.POST['matricula']

        try:
            Doctor.objects.create(Name=n,mobile=m,special=sp,matricula=mat)
            error = "no"
        except:
            error ="yes"
    d = {'error':error}
    return render(request, 'add_doctor.html', d)

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Patient.objects.all()
    d = {'doc': doc}
    return render(request, 'view_patient.html',d)

def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def Add_Patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST['name']
        g = request.POST['gender']
        m = request.POST['mobile']
        a = request.POST['address']

        try:
            Patient.objects.create(name=n,gender=g,mobile=m,address=a)
            error = "no"
        except:
            error ="yes"
    d = {'error':error}
    return render(request, 'add_patient.html', d)

def Add_Appointment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    doctor1=Doctor.objects.all()
    patient1=Patient.objects.all()


    if request.method == "POST":
        n = request.POST['doctor']
        p = request.POST['patient']
        da = request.POST['date']
        t = request.POST['time']
        
        doctor=Doctor.objects.filter(Name=n).first()
        patient=Patient.objects.filter(name=p).first()

        try:
            Appointment.objects.create(doctor=doctor,patient=patient,date=da,time=t)
            error = "no"
        except:
            error ="yes"
    d = {'doctor':doctor1,'patient':patient1,'error':error}
    return render(request, 'add_appointment.html', d)

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Appointment.objects.all()
    d = {'doc': doc}
    return render(request, 'view_appointment.html',d)

def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    app = Appointment.objects.get(id=pid)
    app.delete()
    return redirect('view_appointment')

def Add_Informe(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        nom = request.POST['Nombre']
        ed = request.POST['Edad']
        med = request.POST['Medico']
        hosp = request.POST['Hospital']
        mues = request.POST['Muestra']
        diag = request.POST['Diagnostico']

        fecmues = request.POST['TomaDeMuestra']
        rec = request.POST['Recepcion']
        numlam = request.POST['NumeroDeLaminas']
        tinc = request.POST['Tincion']
        # sp = request.POST['special']

        try:
            PacienteGenerales.objects.create(Nombre=nom,Edad=ed,Medico=med,Hospital=hosp,Muestra=mues,Diagnostico=diag)
            Muestra.objects.create(TomaDeMuestra=fecmues,Recepcion=rec,NumeroDeLaminas=numlam,Tincion=tinc)
            # Informe.objects.create(PacienteInforme.Nombre=nom,PacienteGenerales.Edad=ed)# Doctor.objects.create(Name=n,mobile=m,special=sp)
            error = "no"
        except:
            error ="yes"
        

        lastPaciente=PacienteGenerales.objects.last()
        lastMuestra=Muestra.objects.last()

        try:
            Informe.objects.create(PacienteInforme=lastPaciente,MuestraInforme=lastMuestra)
            error = "no"
        except:
            error ="yes"

    d = {'error':error}
    return render(request, 'add_informe.html', d)

def View_Informe(request):
    if not request.user.is_staff:
        return redirect('login')
    inf = InformeCito.objects.all()
    # pac = PacienteGenerales.objects.all()
    # mue = Muestra.objects.all()
    # p = {'pac': pac}
    # m = {'mue': mue}
    i = {'inf': inf}

    return render(request, 'view_informe.html',i)

def Delete_Informe(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    inf = Informe.objects.get(id=pid)
    # logging.debug()
    paciente_del = inf.PacienteInforme.id
    pac = PacienteGenerales.objects.get(id=paciente_del)

    muestra_del = inf.MuestraInforme.id
    mue = Muestra.objects.get(id=muestra_del)
    
    inf.delete()
    pac.delete()
    mue.delete()
    return redirect('view_informe')

def Ver_Informe(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    # inf = Informe.objects.all()
    # pac = PacienteGenerales.objects.all()
    # mue = Muestra.objects.all()
    # p = {'pac': pac}
    # m = {'mue': mue}
    # i = {'inf': inf}
    paciente = InformeCito.objects.get(id=pid)
    i = {'paciente': paciente}

    return render(request, 'ver_informe.html',i)

def Report(request,pid,opt):
    # Create a file-like buffer to receive PDF data.
    locale.setlocale(locale.LC_ALL, 'es_BO.utf8')
    paciente = InformeCito.objects.get(id=pid)
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer,pagesize=letter)
    # canvas = canvas.Canvas('myfile.pdf', pagesize=letter)
    width, height = letter

    my_Style=ParagraphStyle('Mine', alignment=TA_CENTER, fontName='Helvetica', fontSize = 10)
    p1=Paragraph('''<u>INFORME CITOLOGICO</u>''',my_Style)
    p1.wrapOn(p,width,10)
    p1.drawOn(p,0,26*cm)

    my_Style2=ParagraphStyle('Mine2', alignment=TA_LEFT, fontName='Helvetica', fontSize = 10)
    styles = getSampleStyleSheet()
    style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)

    tbl_data = [[Paragraph("Nombre:"+' '+paciente.PacienteInformeCito.Nombres+'  '+paciente.PacienteInformeCito.Apellidos, my_Style2), 
    Paragraph("Edad:"+' '+ str(paciente.PacienteInformeCito.Edad)+ "años", my_Style2)], 
    [Paragraph("Medico:"+' '+ paciente.PacienteInformeCito.Medico, my_Style2), 
    Paragraph("Hospital/Clinica:"+' '+paciente.PacienteInformeCito.Hospital, my_Style2)], 
    [Paragraph("Muestra:"+' '+ paciente.PacienteInformeCito.Muestra, my_Style2), 
    Paragraph("Diagnostico:"+' '+paciente.PacienteInformeCito.Diagnostico, my_Style2)]]
    tbl = Table(tbl_data)
    tbl.wrapOn(p,width-2*cm,3*cm)
    tbl.drawOn(p,1*cm,23*cm)

    p.line(0+1*cm,22.5*cm,width-1*cm,22.5*cm)

    tbl_data_2 = [[Paragraph("Toma de muestra:"+' '+ str(paciente.MuestraInformeCito.TomaDeMuestra.strftime("%d-%m-%Y")), my_Style2), 
    Paragraph("Recepcion:"+' '+ str(paciente.MuestraInformeCito.Recepcion.strftime("%d-%m-%Y")), my_Style2)], 
    [Paragraph("N° de laminas:"+' '+ str(paciente.MuestraInformeCito.NumeroDeLaminas), 
    my_Style2), Paragraph("Tincion:"+' '+paciente.MuestraInformeCito.Tincion, my_Style2)]]
    tbl_2 = Table(tbl_data_2)
    tbl_2.wrapOn(p,width-2*cm,3*cm)
    tbl_2.drawOn(p,1*cm,20.75*cm)

    p2=Paragraph('''<img src="hospital/static/images/logo.jpg" width="100" height="80"/>''', style=styles["Normal"])
    p2.wrapOn(p,width,10)
    p2.drawOn(p,1*cm,25*cm)

    my_Style_suelto=ParagraphStyle('Mine', alignment=TA_LEFT, fontName='Helvetica', fontSize = 10)
    p3=Paragraph("ESTUDIO MISCROSCÓPICO:"+' '+ paciente.EstudioMicroscopicoInformeCito.get_Descripcion_display(),my_Style_suelto)
    p3.wrapOn(p,width-2*cm,2*cm)
    p3.drawOn(p,1*cm,19.75*cm)

    # data=[['I. Calidad de Muestra ', '', '02'], ['II. Microorganismos', '', '12'],
    # ['', '21', '22'], ['III. Valoración Citológica', '21', '22'], 
    # ['IV. Hallazgos no neoplasicos ', '31', '32'],
    # ['V. Evaluacion Hormonal ', '31', '32'],]
    # t=Table(data,style=[('GRID',(0,0),(-1,-1),0.5,colors.grey),('SPAN',(0,1),(0,2))])
    # t.wrapOn(p,width-2*cm,5*cm)
    # t.drawOn(p,1*cm,8.75*cm)

    tbl_data_3=[['I. Calidad de Muestra', Paragraph(paciente.CalidadDeMuestraInformeCito.get_Calidad_display(),my_Style2), ''],
    ['II. Microorganismos', Paragraph(paciente.MicrorganismosInformeCito.get_Microrgs_display(),my_Style2),''], 
    ['III. Hallazgos No Neoplasicos', Paragraph(paciente.HallazgosInformeCito.get_NoNeoplasicos_display(),my_Style2),''],
    ['IV. Anomalia de Células Epiteliales', 'Celulas Escamosas', Paragraph(paciente.CelEscamosasInformeCito.get_Escamosas_display(),my_Style2)],
    ['', 'Células Glandulares', Paragraph(paciente.CelGlandularesInformeCito.get_Glandulares_display(),my_Style2)], 
    ['V. Inflamación ', Paragraph(paciente.InflamacionInformeCito.get_Inflamation_display(),my_Style2), '32'],
    ['VI. Patrón Hormonal ', Paragraph(paciente.EvaluacionHormonalInformeCito.get_Evaluacion_display(),my_Style2), '32'],]
    tbl_3=Table(tbl_data_3,style=[('GRID',(0,0),(-1,-1),1,colors.black),('SPAN',(0,3),(0,4)),('SPAN',(1,0),(2,0)),('SPAN',(1,1),(2,1)),('SPAN',(1,2),(2,2)),('SPAN',(1,5),(2,5)),('SPAN',(1,6),(2,6)),('SPAN',(1,7),(2,7))])
    tbl_3.wrapOn(p,width-2*cm,8*cm)
    tbl_3.drawOn(p,1*cm,14*cm)

    p4=Paragraph('''<b>CONCLUSION:</b>'''+''+ paciente.ConclusionInformeCito.get_Conclusion_display(),my_Style_suelto)
    p4.wrapOn(p,width-2*cm,2*cm)
    p4.drawOn(p,1*cm,13*cm)

    p5=Paragraph('Recomendación: '+' '+ paciente.RecomendacionInformeCito.Recomendacion,my_Style_suelto)
    p5.wrapOn(p,width-2*cm,2*cm)
    p5.drawOn(p,1*cm,12*cm)

    p6=Paragraph(paciente.LugarInformeCito.get_Lugar_display()+', '+str(paciente.FechaPieInformeCito.Fecha.strftime("%B %d, %Y")),my_Style_suelto)
    p6.wrapOn(p,width-2*cm,2*cm)
    p6.drawOn(p,1*cm,8*cm)

    my_Style_suelto_der=ParagraphStyle('Mine', alignment=TA_RIGHT, fontName='Helvetica', fontSize = 10)
    
    if opt==2:

        p7=Paragraph(paciente.DoctorInformeCito.Name,my_Style_suelto_der )
        p7.wrapOn(p,width-2*cm,2*cm)
        p7.drawOn(p,1*cm,7*cm)
    
        p8=Paragraph(paciente.DoctorInformeCito.special,my_Style_suelto_der )
        p8.wrapOn(p,width-2*cm,2*cm)
        p8.drawOn(p,1*cm,6.5*cm)

        p9=Paragraph(paciente.DoctorInformeCito.matricula,my_Style_suelto_der )
        p9.wrapOn(p,width-2*cm,2*cm)
        p9.drawOn(p,1*cm,6*cm)

    p10=Paragraph(paciente.CodigoInformeCito.Codigo,my_Style_suelto_der )
    p10.wrapOn(p,width-2*cm,2*cm)
    p10.drawOn(p,1*cm,25*cm)
    
    if opt == 1:
        p11=Paragraph('''<img src="hospital/static/images/firma_crop.jpeg" width="100" height="80"/>''', style_right)
        p11.wrapOn(p,width-2*cm,2*cm)
        p11.drawOn(p,1*cm,6*cm)
    
    textob=p.beginText()
    textob.setTextOrigin(cm,cm)
    textob.setFont("Helvetica",14)
    
    # lines=["This is line 1","This is line 2","This is line 3"]

    # for line in lines:
    #     textob.textLine(line)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    
    
    
    # p.drawCentredString(width/2, 26*cm,"INFORME CITOLOGICO")
    p.setTitle("INFORME CITOLOGICO")
    
    # p.drawString(100, 50, paciente.PacienteInformeCito.Nombres)
    # p.line()

    # Close the PDF object cleanly, and we're done.
    p.drawText(textob)
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='INFORME_CITOLOGICO.pdf')

def Add_Informe_Cit(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    Estudio_form = EstudioMicroscopico.DESCRIPCIONES
    Calidad_form= CalidadDeMuestra.CALIDADES
    Microrganismos_form = Microrganismos.MICROS
    Hallazgos_form = HallazgosNoNeoplasicos.HALLAZGOS
    CelEscamosas_form = CelEscamosas.ESCAMOSAS
    CelGlandulares_form = CelGlandulares.GLANDULARES
    EvaluacionHormonal_form = EvaluacionHormonal.EVAL
    Inflamacion_form = Inflamacion.INFL
    Conclu_form = Conclusion.CONCLU
    Lugar_form = Lugar.LUGARES
    doctor1=Doctor.objects.all()


    if request.method == "POST":
        
        cod=request.POST['Codigo']
        
        nom = request.POST['Nombres']
        ape = request.POST['Apellidos']
        ed = request.POST['Edad']
        med = request.POST['Medico']
        hosp = request.POST['Hospital']
        mues = request.POST['Muestra']
        diag = request.POST['Diagnostico']

        fecmues = request.POST['TomaDeMuestra']
        # fecmues2= fecmues.strftime("%d/%m/%Y")
        rec = request.POST['Recepcion']
        # rec2 = rec2.strftime("%d/%m/%Y")
        numlam = request.POST['NumeroDeLaminas']
        tinc = request.POST['Tincion']

        estmic = request.POST['Descripcion']
        calid = request.POST['CalidadDeMuestra']
        micro = request.POST['Microrganismos']
        hall = request.POST['Hallazgos']
        esc = request. POST['CelEscamosas']
        glan = request.POST['CelGlandulares']
        evalu = request.POST['EvaluacionHormonal']
        infla = request.POST['Inflamacion']
        conclu = request.POST['Conclusion']
        recomend = request.POST['Recomendacion']
        fech = request.POST['FechaPie']
        # fech2 = fech.strftime("%d/%m/%Y")
        lug = request.POST['Lugar']

        n = request.POST['doctor']

        doctor=Doctor.objects.filter(Name=n).first()

        try:
            CodigoInforme.objects.create(Codigo=cod)
            PacienteGenerales.objects.create(Nombres=nom,Apellidos=ape,Edad=ed,Medico=med,Hospital=hosp,Muestra=mues,Diagnostico=diag)
            Muestra.objects.create(TomaDeMuestra=fecmues,Recepcion=rec,NumeroDeLaminas=numlam,Tincion=tinc)
            EstudioMicroscopico.objects.create(Descripcion=estmic)
            CalidadDeMuestra.objects.create(Calidad=calid)
            Microrganismos.objects.create(Microrgs=micro)
            HallazgosNoNeoplasicos.objects.create(NoNeoplasicos=hall)
            CelEscamosas.objects.create(Escamosas=esc)
            CelGlandulares.objects.create(Glandulares=glan)
            EvaluacionHormonal.objects.create(Evaluacion=evalu)
            Inflamacion.objects.create(Inflamation=infla)
            Conclusion.objects.create(Conclusion=conclu)
            Recomendacion.objects.create(Recomendacion=recomend)
            FechaPie.objects.create(Fecha=fech)
            Lugar.objects.create(Lugar=lug)

            # Informe.objects.create(PacienteInforme.Nombre=nom,PacienteGenerales.Edad=ed)# Doctor.objects.create(Name=n,mobile=m,special=sp)
            error = "no"
        except:
            error ="yes"
        
        # try:
            # Muestra.objects.create(TomaDeMuestra=fecmues,Recepcion=rec,NumeroDeLaminas=numlam,Tincion=tinc)
            # error = "no"
        # except:
            # error="yes"


        lastCodigo=CodigoInforme.objects.last()
        lastPaciente=PacienteGenerales.objects.last()
        lastMuestra=Muestra.objects.last()
        lastEstudioMicroscopico=EstudioMicroscopico.objects.last()
        lastCalidadDeMuestra=CalidadDeMuestra.objects.last()
        lastMicrorganismos=Microrganismos.objects.last()
        lastHallazgos=HallazgosNoNeoplasicos.objects.last()
        lastCelEscamosas=CelEscamosas.objects.last()
        lastCelGlandulares=CelGlandulares.objects.last()
        lastEvaluacionHormonal=EvaluacionHormonal.objects.last()
        lastInflamacion=Inflamacion.objects.last()
        lastConclusion=Conclusion.objects.last()
        lastRecomendacion=Recomendacion.objects.last()
        lastFechaPie=FechaPie.objects.last()
        lastLugar=Lugar.objects.last()

        try:
            InformeCito.objects.create(CodigoInformeCito=lastCodigo,PacienteInformeCito=lastPaciente,MuestraInformeCito=lastMuestra,
            EstudioMicroscopicoInformeCito=lastEstudioMicroscopico,CalidadDeMuestraInformeCito=lastCalidadDeMuestra, 
            HallazgosInformeCito=lastHallazgos, MicrorganismosInformeCito=lastMicrorganismos,CelEscamosasInformeCito=lastCelEscamosas,
            CelGlandularesInformeCito=lastCelGlandulares,EvaluacionHormonalInformeCito=lastEvaluacionHormonal,
            InflamacionInformeCito=lastInflamacion,ConclusionInformeCito=lastConclusion,
            RecomendacionInformeCito=lastRecomendacion,FechaPieInformeCito=lastFechaPie,
            LugarInformeCito=lastLugar,DoctorInformeCito=doctor)
            error = "no"
        except:
            error ="yes"

    d = {'estmicroscopico':Estudio_form,'calidad':Calidad_form,'microrgs':Microrganismos_form, 'hallazgos':Hallazgos_form,'escamosas':CelEscamosas_form , 'glandulares':CelGlandulares_form, 'evaluacion':EvaluacionHormonal_form,'inflamacion': Inflamacion_form,'conclusion':Conclu_form,'lugar':Lugar_form,'doctor':doctor1,'error':error}
    # d = {'error':error}

    return render(request, 'add_informe_cit.html', d)

def Upd_Datos_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCito.objects.get(id=pid)

    cod_del_id = paciente.CodigoInformeCito.id
    cod_upd = CodigoInforme.objects.get(id=cod_del_id)

    gen_id = paciente.PacienteInformeCito.id
    pac_upd = PacienteGenerales.objects.get(id=gen_id)
    
    if request.method == "POST":
        
        cod=request.POST['Codigo']
        
        nom = request.POST['Nombres']
        ape = request.POST['Apellidos']
        ed = request.POST['Edad']
        med = request.POST['Medico']
        hosp = request.POST['Hospital']
        mues = request.POST['Muestra']
        diag = request.POST['Diagnostico']

        
        try:
            paciente.CodigoInformeCito.Codigo=cod
            paciente.PacienteInformeCito.Nombres=nom
            paciente.PacienteInformeCito.Apellidos=ape
            paciente.PacienteInformeCito.Edad=ed
            paciente.PacienteInformeCito.Medico=med
            paciente.PacienteInformeCito.Hospital=hosp
            paciente.PacienteInformeCito.Muestra=mues
            paciente.PacienteInformeCito.Diagnostico=diag
            paciente.save()
            cod_upd.Codigo=cod
            cod_upd.save()
            pac_upd.Nombres=nom
            pac_upd.Apellidos=ape
            pac_upd.Edad=ed
            pac_upd.Medico=med
            pac_upd.Hospital=hosp
            pac_upd.Muestra=mues
            pac_upd.Diagnostico=diag
            pac_upd.save()


            # CodigoInforme.objects.create(Codigo=cod)
            # PacienteGenerales.objects.create(Nombres=nom,Apellidos=ape,Edad=ed,Medico=med,Hospital=hosp,Muestra=mues,Diagnostico=diag)

            # Informe.objects.create(PacienteInforme.Nombre=nom,PacienteGenerales.Edad=ed)# Doctor.objects.create(Name=n,mobile=m,special=sp)
            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente}
    return render(request, 'upd_datos_paciente.html', d)

def Upd_Muestra_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCito.objects.get(id=pid)

    fecha_muestra = paciente.MuestraInformeCito.TomaDeMuestra.strftime("%Y-%m-%d")
    fecha_recepcion = paciente.MuestraInformeCito.Recepcion.strftime("%Y-%m-%d")
    

    muestra_del_id = paciente.MuestraInformeCito.id
    muestra_upd = Muestra.objects.get(id=muestra_del_id)
    
    if request.method == "POST":
        
        
        fecmues = request.POST['TomaDeMuestra']
        rec = request.POST['Recepcion']
        numlam = request.POST['NumeroDeLaminas']
        tinc = request.POST['Tincion']

        
        try:
            paciente.MuestraInformeCito.TomaDeMuestra=fecmues
            paciente.MuestraInformeCito.Recepcion=rec
            paciente.MuestraInformeCito.NumeroDeLaminas=numlam
            paciente.MuestraInformeCito.Tincion=tinc
            paciente.save()
            muestra_upd.TomaDeMuestra=fecmues
            muestra_upd.Recepcion=rec
            muestra_upd.NumeroDeLaminas=numlam
            muestra_upd.Tincion=tinc
            muestra_upd.save()
            # CodigoInforme.objects.create(Codigo=cod)
            # PacienteGenerales.objects.create(Nombres=nom,Apellidos=ape,Edad=ed,Medico=med,Hospital=hosp,Muestra=mues,Diagnostico=diag)

            # Informe.objects.create(PacienteInforme.Nombre=nom,PacienteGenerales.Edad=ed)# Doctor.objects.create(Name=n,mobile=m,special=sp)
            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'fecha_muestra':fecha_muestra,'fecha_recepcion':fecha_recepcion}
    return render(request,'upd_muestra_paciente.html', d)

def Upd_Tabla_Central_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCito.objects.get(id=pid)

    Estudio_form = EstudioMicroscopico.DESCRIPCIONES
    Calidad_form= CalidadDeMuestra.CALIDADES
    Microrganismos_form = Microrganismos.MICROS
    Hallazgos_form = HallazgosNoNeoplasicos.HALLAZGOS
    CelEscamosas_form = CelEscamosas.ESCAMOSAS
    CelGlandulares_form = CelGlandulares.GLANDULARES
    EvaluacionHormonal_form = EvaluacionHormonal.EVAL
    Inflamacion_form = Inflamacion.INFL
    

    # muestra_del_id = paciente.MuestraInformeCito.id
    # muestra_upd = Muestra.objects.get(id=muestra_del_id)

    estudio_micros_id = paciente.EstudioMicroscopicoInformeCito.id
    estudio_micros_upd = EstudioMicroscopico.objects.get(id=estudio_micros_id)
    calidad_id = paciente.CalidadDeMuestraInformeCito.id
    calidad_upd = CalidadDeMuestra.objects.get(id=calidad_id)
    microrgs_id = paciente.MicrorganismosInformeCito.id
    microrgs_upd = Microrganismos.objects.get(id=microrgs_id)
    hallazgos_id = paciente.HallazgosInformeCito.id
    hallazgos_upd = HallazgosNoNeoplasicos.objects.get(id=hallazgos_id)
    celescamosas_id = paciente.CelEscamosasInformeCito.id
    celescamosas_upd = CelEscamosas.objects.get(id=celescamosas_id)
    celglandulares_id = paciente.CelGlandularesInformeCito.id
    celglandulares_upd = CelGlandulares.objects.get(id=celglandulares_id)
    eval_hormonal_id = paciente.EvaluacionHormonalInformeCito.id
    eval_hormonal_upd = EvaluacionHormonal.objects.get(id=eval_hormonal_id)
    inflamacion_id = paciente.InflamacionInformeCito.id
    inflamacion_upd = Inflamacion.objects.get(id=inflamacion_id)
    
    
    if request.method == "POST":
        
        estmic = request.POST['Descripcion']
        calid = request.POST['CalidadDeMuestra']
        micro = request.POST['Microrganismos']
        hall = request.POST['Hallazgos']
        esc = request. POST['CelEscamosas']
        glan = request.POST['CelGlandulares']
        evalu = request.POST['EvaluacionHormonal']
        infla = request.POST['Inflamacion']

        
        try:
            paciente.EstudioMicroscopicoInformeCito.Descripcion=estmic
            paciente.CalidadDeMuestraInformeCito.Calidad = calid
            paciente.MicrorganismosInformeCito.Microrgs = micro
            paciente.HallazgosInformeCito.NoNeoplasicos = hall
            paciente.CelEscamosasInformeCito.Escamosas = esc
            paciente.CelGlandularesInformeCito.Glandulares = glan
            paciente.EvaluacionHormonalInformeCito.Evaluacion = evalu
            paciente.InflamacionInformeCito.Inflamation = infla
            paciente.save()

            estudio_micros_upd.Descripcion=estmic
            estudio_micros_upd.save()
            calidad_upd.Calidad=calid
            calidad_upd.save()
            microrgs_upd.Microrgs = micro
            microrgs_upd.save()
            hallazgos_upd.Neoplasicos = hall
            hallazgos_upd.save()
            celescamosas_upd.Escamosas = esc
            celescamosas_upd.save()
            celglandulares_upd.Glandulares = glan
            celglandulares_upd.save()
            eval_hormonal_upd.Evaluacion = evalu
            eval_hormonal_upd.save()
            inflamacion_upd.Inflamation = infla
            inflamacion_upd.save()

            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'estmicroscopico':Estudio_form,'calidad':Calidad_form,
    'microrgs':Microrganismos_form, 'hallazgos':Hallazgos_form,'escamosas':CelEscamosas_form , 
    'glandulares':CelGlandulares_form, 'evaluacion':EvaluacionHormonal_form,
    'inflamacion': Inflamacion_form}
    return render(request,'upd_tabla_central_paciente.html', d)

def Upd_Conclusion_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCito.objects.get(id=pid)

    Conclu_form = Conclusion.CONCLU
    Lugar_form = Lugar.LUGARES

    fecha_informe = paciente.FechaPieInformeCito.Fecha.strftime("%Y-%m-%d")
    

    # muestra_del_id = paciente.MuestraInformeCito.id
    # muestra_upd = Muestra.objects.get(id=muestra_del_id)

    conclu_id = paciente.ConclusionInformeCito.id
    conclu_upd = Conclusion.objects.get(id=conclu_id)
    recomendacion_id = paciente.RecomendacionInformeCito.id
    recomendacion_upd = Recomendacion.objects.get(id=recomendacion_id)
    lugar_id = paciente.LugarInformeCito.id
    lugar_upd = Lugar.objects.get(id=lugar_id)
    fechapie_id = paciente.FechaPieInformeCito.id
    fechapie_upd = FechaPie.objects.get(id=fechapie_id)
    
    if request.method == "POST":
        
        conclu = request.POST['Conclusion']
        recomend = request.POST['Recomendacion']
        fech = request.POST['FechaPie']
        lug = request.POST['Lugar']
        
        try:
            paciente.ConclusionInformeCito.Conclusion = conclu
            paciente.RecomendacionInformeCito.Recomendacion = recomend
            paciente.FechaPieInformeCito.Fecha = fech
            paciente.LugarInformeCito.Lugar = lug
            paciente.save()

            conclu_upd.Conclusion = conclu
            conclu_upd.save()
            recomendacion_upd.Recomendacion = recomend
            recomendacion_upd.save()
            fechapie_upd.Fecha = fech
            fechapie_upd.save()
            lugar_upd.Lugar = lug
            lugar_upd.save()

            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'conclusion':Conclu_form,'lugar':Lugar_form,'fechainf':fecha_informe}
    return render(request,'upd_conclusion_paciente.html', d)