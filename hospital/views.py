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

        try:
            Doctor.objects.create(Name=n,mobile=m,special=sp)
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
    inf = Informe.objects.all()
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
    paciente = Informe.objects.get(id=pid)
    i = {'paciente': paciente}

    return render(request, 'ver_informe.html',i)

# def Report(request):
#     sales = [
#         {"item": "Keyboard", "amount": "$120,00"},
#         {"item": "Mouse", "amount": "$10,00"},
#         {"item": "House", "amount": "$1 000 000,00"},
#     ]
#     pdf = FPDF('P', 'mm', 'A4')
#     pdf.add_page()
#     pdf.set_font('courier', 'B', 16)
#     pdf.cell(40, 10, 'This is what you have sold this month so far:',0,1)
#     pdf.cell(40, 10, '',0,1)
#     pdf.set_font('courier', '', 12)
#     pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
#     pdf.line(10, 30, 150, 30)
#     pdf.line(10, 38, 150, 38)
#     for line in sales:
#         pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)

#     pdf.output('tuto1.pdf', 'F')
#     return render(request, "index.html")

def Report(request,pid):
    # Create a file-like buffer to receive PDF data.
    paciente = Informe.objects.get(id=pid)
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

    tbl_data = [[Paragraph("Nombre:"+paciente.PacienteInforme.Nombres+paciente.PacienteInforme.Apellidos, my_Style2), Paragraph("Edad:"+ str(paciente.PacienteInforme.Edad)+ "años", my_Style2)], 
    [Paragraph("Medico:"+ paciente.PacienteInforme.Medico, my_Style2), Paragraph("Hospital/Clinica:"+paciente.PacienteInforme.Hospital, my_Style2)], 
    [Paragraph("Muestra:"+ paciente.PacienteInforme.Muestra, my_Style2), Paragraph("Diagnostico:"+paciente.PacienteInforme.Diagnostico, my_Style2)]]
    tbl = Table(tbl_data)
    tbl.wrapOn(p,width-2*cm,3*cm)
    tbl.drawOn(p,1*cm,23*cm)

    p.line(0+1*cm,22.5*cm,width-1*cm,22.5*cm)

    tbl_data_2 = [[Paragraph("Toma de muestra:"+ str(paciente.MuestraInforme.TomaDeMuestra), my_Style2), Paragraph("Recepcion:"+ str(paciente.MuestraInforme.Recepcion), my_Style2)], 
    [Paragraph("N° de laminas:"+ str(paciente.MuestraInforme.NumeroDeLaminas), my_Style2), Paragraph("Tincion:"+paciente.MuestraInforme.Tincion, my_Style2)]]
    tbl_2 = Table(tbl_data_2)
    tbl_2.wrapOn(p,width-2*cm,3*cm)
    tbl_2.drawOn(p,1*cm,20.75*cm)

    p2=Paragraph('''<img src="hospital/static/images/logo.jpg" width="100" height="80"/>''', style=styles["Normal"])
    p2.wrapOn(p,width,10)
    p2.drawOn(p,1*cm,25*cm)

    
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
    
    p.drawString(100, 50, paciente.PacienteInforme.Nombres)
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
        rec = request.POST['Recepcion']
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