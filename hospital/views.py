from django.shortcuts import render, redirect
# from django.fpdf2 import FPDF
# import io
# from django.http import FileResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Doctor,Patient,Appointment,PacienteGenerales,Muestra, Informe
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

def Report(request):
    return (request,'ver_informe.html')
