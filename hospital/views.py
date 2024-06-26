from django.shortcuts import render, redirect

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
from .models import Doctor

from .models import InformeAnatomico, InformeCitologico
import logging


def About(request):
    return render (request,'about.html') 

def Home(request):
    return render (request,'home.html')

def Contact(request):
    return render (request,'contact.html')

def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    info_anato = InformeAnatomico.objects.all()
    info_cito = InformeCitologico.objects.all()
    d=0
    p=0
    for i in info_anato:
        d+=1
    
    for i in info_cito:
        p+=1
    
    d1={'d':d,'p':p}

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



def View_Informe(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    inf = InformeCitologico.objects.all()
    i = {'inf': inf}

    return render(request, 'view_informe.html',i)



def Ver_Informe(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    paciente = InformeCitologico.objects.get(id=pid)
    i = {'paciente': paciente}

    return render(request, 'ver_informe.html',i)

def Report(request,pid):   
    error = ""
    # Create a file-like buffer to receive PDF data.
    if request.method == "POST":
        
        firma = request.POST['firma']
        logo = request.POST['logo']
        
        locale.setlocale(locale.LC_ALL, 'es_BO.utf8')
        paciente = InformeCitologico.objects.get(id=pid)   
        buffer = io.BytesIO()           
        # Create the PDF object,     using the buffer as its "file."
        p = canvas.Canvas(buffer,pagesize=letter)
        # canvas = canvas.Canvas('myfile.pdf', pagesize=letter)
        width, height = letter
        
        c=4.5

        my_Style=ParagraphStyle('Mine', alignment=TA_CENTER, fontName='Helvetica', fontSize = 10)
        p1=Paragraph('''<b><u>REPORTE DE CITOLOGÍA CERVICO-VAGINAL</u></b>'''+'<br />\n'+ '''<b><u>SISTEMA BETHESDA </u></b>''' ,my_Style)
        p1.wrapOn(p,width,10)
        p1.drawOn(p,0,height-c*cm)

        my_Style2=ParagraphStyle('Mine2', alignment=TA_LEFT, fontName='Helvetica', fontSize = 10)
        styles = getSampleStyleSheet()
        style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)

        m=1.5
         
        tbl_data = [[Paragraph("Nombre:"+' '+paciente.NombresInformeCitologico+ '  '+paciente.ApellidosInformeCitologico, my_Style2), 
        Paragraph("Edad:"+' '+ str(paciente.EdadInformeCitologico)+ "años", my_Style2)], 
        [Paragraph("Medico:"+' '+ paciente.MedicoInformeCitologico, my_Style2), 
        Paragraph("Hospital/Clinica:"+' '+paciente.HospitalInformeCitologico, my_Style2)], 
        [Paragraph("Muestra:"+' '+ paciente.MuestraInformeCitologico, my_Style2), 
        Paragraph("Diagnostico:"+' '+paciente.DiagnosticoInformeCitologico, my_Style2)]]
        tbl = Table(tbl_data)
        tbl.wrapOn(p,width-4*cm,3*cm)
        tbl.drawOn(p,2*cm,(22-m)*cm)

        p.line(0+2*cm,(22.625-m)*cm,width-2*cm,(22.625-m)*cm)
    
        tbl_data_2 = [[Paragraph("Toma de muestra:"+' '+ str(paciente.TomaDeMuestraInformeCitologico.strftime("%d-%m-%Y")), my_Style2), 
        Paragraph("Recepcion:"+' '+ str(paciente.RecepcionInformeCitologico.strftime("%d-%m-%Y")), my_Style2)], 
        [Paragraph("N° de laminas:"+' '+ str(paciente.NumeroDeLaminasInformeCitologico), 
        my_Style2), Paragraph("Tincion:"+' '+paciente.TincionInformeCitologico, my_Style2)]]
        tbl_2 = Table(tbl_data_2)
        tbl_2.wrapOn(p,width-4*cm,3*cm)
        tbl_2.drawOn(p,2*cm,(20.75-m)*cm)
    
        if logo == "SI": 
            p2=Paragraph('''<img src="hospital/static/images/logo.jpg" width="100" height="80"/>''', style=styles["Normal"])
            p2.wrapOn(p,width,10)
            p2.drawOn(p,2.5*cm,height-c*cm)
    
        my_Style_suelto=ParagraphStyle('Mine', alignment=TA_LEFT, fontName='Helvetica', fontSize = 10)
        p3=Paragraph('''<b>ESTUDIO MICROSCOPICO:</b>'''+' '+ paciente.EstudioMicroscopicoInformeCitologico,my_Style_suelto)
        p3.wrapOn(p,width-4*cm,2*cm)
        p3.drawOn(p,2*cm,(19.75-m)*cm)
    
        p.line(0+2*cm,(20.5-m)*cm,width-2*cm,(20.5-m)*cm)
        p3=Paragraph('''<b>CALIDAD DE MUESTRA:</b>'''+'<br />\n'+ paciente.CalidadDeMuestraInformeCitologico,my_Style_suelto)
        p3.wrapOn(p,width-4*cm,2*cm)
        p3.drawOn(p,2*cm,(18-m)*cm)
        
        k=1.5
        a=k
        
        if paciente.MicrorganismosInformeCitologico != 'NO INCLUIR':
            p3_1 = Paragraph('''<b>MICROORGANISMOS:</b>'''+'<br />\n'+ paciente.MicrorganismosInformeCitologico,my_Style_suelto)
            p3_1.wrapOn(p,width-4*cm,2*cm)
            p3_1.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k
    
        if paciente.HallazgosInformeCitologico != 'NO INCLUIR':
            p3_2 = Paragraph('''<b>HALLAZGOS NO NEOPLASICOS:</b>'''+'<br />\n'+ paciente.HallazgosInformeCitologico,my_Style_suelto)
            p3_2.wrapOn(p,width-4*cm,2*cm)
            p3_2.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k
        
        if paciente.CelEscamosasInformeCitologico != 'NO INCLUIR' and paciente.CelGlandularesInformeCitologico != 'NO INCLUIR':
            a = a+k
            p3_3 = Paragraph( '''<b>VALORACION CITOLOGICA:</b>''' +'<br />\n'+ '''<b>CELULAS ESCAMOSAS:</b>''' +'<br />\n'+ paciente.CelEscamosasInformeCitologico +'<br />\n'+ '''<b>CELULAS GLANDULARES:</b>''' +'<br />\n'+ paciente.CelGlandularesInformeCitologico,my_Style_suelto)
            p3_3.wrapOn(p,width-4*cm,2*cm)
            p3_3.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k
    
        if paciente.CelEscamosasInformeCitologico != 'NO INCLUIR' and paciente.CelGlandularesInformeCitologico == 'NO INCLUIR':
            p3_4 = Paragraph( '''<b>VALORACION CITOLOGICA:</b>''' +'<br />\n'+ '''<b>CELULAS ESCAMOSAS:</b>''' +'<br />\n'+ paciente.CelEscamosasInformeCitologico ,my_Style_suelto)
            p3_4.wrapOn(p,width-4*cm,2*cm)
            p3_4.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k

        if paciente.CelEscamosasInformeCitologico == 'NO INCLUIR' and paciente.CelGlandularesInformeCitologico != 'NO INCLUIR':
            p3_5 = Paragraph( '''<b>VALORACION CITOLOGICA:</b>''' +'<br />\n'+ '''<b>CELULAS GLANDULARES:</b>''' +'<br />\n'+ paciente.CelGlandularesInformeCitologico,my_Style_suelto)
            p3_5.wrapOn(p,width-4*cm,2*cm)
            p3_5.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k    

        if paciente.InflamacionInformeCitologico != 'NO INCLUIR':
            p3_6 = Paragraph('''<b>INFLAMACION:</b>'''+'<br />\n'+ paciente.InflamacionInformeCitologico,my_Style_suelto)
            p3_6.wrapOn(p,width-4*cm,2*cm)
            p3_6.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k

        if paciente.EvaluacionHormonalInformeCitologico != 'NO INCLUIR':
            p3_7 = Paragraph('''<b>EVALUACION HORMONAL:</b>'''+'<br />\n'+ paciente.EvaluacionHormonalInformeCitologico,my_Style_suelto)
            p3_7.wrapOn(p,width-4*cm,2*cm)
            p3_7.drawOn(p,2*cm,(18-a-m)*cm)
            a = a+k


        p.line(0+2*cm,(7.5-m)*cm,width-2*cm,(7.5-m)*cm)

        if paciente.ConclusionInformeCitologico != 'NO INCLUIR':
            p4=Paragraph('''<b>CONCLUSION:</b>'''+''+ paciente.ConclusionInformeCitologico,my_Style_suelto)
            p4.wrapOn(p,width-4*cm,2*cm)
            p4.drawOn(p,2*cm,(7-m)*cm)

        p5=Paragraph('''<b>RECOMENDACION:</b>'''+' '+ paciente.RecomendacionInformeCitologico,my_Style_suelto)
        p5.wrapOn(p,width-4*cm,2*cm)
        p5.drawOn(p,2*cm,(6-m)*cm)

        p6=Paragraph(paciente.LugarInformeCitologico+', '+str(paciente.FechaPieInformeCitologico.strftime("%B %d, %Y")),my_Style_suelto)
        p6.wrapOn(p,width-4*cm,2*cm)
        p6.drawOn(p,2*cm,(5-m)*cm)

        my_Style_suelto_der=ParagraphStyle('Mine', alignment=TA_RIGHT, fontName='Helvetica', fontSize = 10)

        if firma == 'NO':

            p7=Paragraph(paciente.DoctorInformeCitologico.Name,my_Style_suelto_der )
            p7.wrapOn(p,width-4*cm,2*cm)
            p7.drawOn(p,2*cm,3*cm)

            p8=Paragraph(paciente.DoctorInformeCitologico.special,my_Style_suelto_der )
            p8.wrapOn(p,width-4*cm,2*cm)
            p8.drawOn(p,2*cm,2.5*cm)

            p9=Paragraph(paciente.DoctorInformeCitologico.matricula,my_Style_suelto_der )
            p9.wrapOn(p,width-4*cm,2*cm)
            p9.drawOn(p,2*cm,2*cm)

        p10=Paragraph(paciente.CodigoInformeCitologico,my_Style_suelto_der )
        p10.wrapOn(p,width-4*cm,2*cm)
        p10.drawOn(p,2*cm,height-c*cm)

        if firma == 'SI':
            p11=Paragraph('''<img src="hospital/static/images/FIRMA_BN.jpeg" width="100" height="80"/>''', style_right)
            p11.wrapOn(p,width-4*cm,2*cm)
            p11.drawOn(p,2*cm,2*cm)
    
        p.line(0+2*cm,1.5*cm,width-2*cm,1.5*cm)
        p12=Paragraph('Direccion: Z/villa dolores, calle 6. No 50. Piso 2 Oficina 8',my_Style_suelto)
        p12.wrapOn(p,width-4*cm,2*cm)
        p12.drawOn(p,2*cm,1*cm)
        
        textob=p.beginText()
        textob.setTextOrigin(cm,cm)
        textob.setFont("Helvetica",14)
    
        p.setTitle("INFORME_CITOLOGICO"+'_'
                   +paciente.ApellidosInformeCitologico+'_'
                   +str(paciente.FechaPieInformeCitologico.strftime("%B_%d_%Y")))
        
        title = "INFORME_CITOLOGICO"+'_'+paciente.ApellidosInformeCitologico+'_'+str(paciente.FechaPieInformeCitologico.strftime("%B_%d_%Y")) +".pdf"

        p.drawText(textob)
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=title)
    
    d = {'error':error}
    return render(request, 'report_signature_logo.html',d)

def Add_Informe_Cit(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    vector_estudio = ["EXTENDIDO CITOLÓGICO CONVENCIONAL: EXO-ENDOCERVICAL",
                      "EXTENDIDO CITOLÓGICO POST- HISTERECTOMIA"]
    
    vector_calidad = ["SATISFACTORIO PARA VALORACIÓN CITOLÓGICA: CON PRESENCIA DE CELULAS EPITELIALES DE LA ZONA DE TRANSFORMACIÓN",
                      "SATISFACTORIO PARA VALORACIÓN CITOLÓGICA" , 
                      "INSATISFACTORIO POR AUSENCIA DE CÉLULAS EXOCERVICALES",
                      "INSATISFACTORIO POR PRESENCIA DE ESCASAS CÉLULAS EXOCERVICALES",
                      "INSATISFACTORIO POR MAS DEL 75% DE CÉLULAS CUBIERTA POR HEMATIES",
                      "INSATISFACTORIO POR MAS DEL 75% DE CÉLULAS CUBIERTAS POR INFLAMACIÓN",
                      "INSATISFACTORIO POR MAS DEL 75% DE CÉLULAS CUBIERTAS POR HEMATIES E INFLAMACIÓN"]
    
    vector_microorganismos = ["FLORA HABITUAL","FLORA BACTERIANA MIXTA",
        "FLORA COCOIDE","CAMBIOS EN LA FLORA SUGESTIVOS DE VAGINOSIS BACTERIANA",       
        "TRICHOMONAS VAGINALIS","ORGANISMOS MICÓTICOS MORFOLOGICAMENTE COMPATIBLES CON CANDIDA SP",
        "BACTERIAS MORFOLOGICAMENTE COMPATIBLES CON ACTYNOMICES SP",
        "CAMBIOS COMPATIBLES CON VIRUS HERPES SIMPLE",
        "NO INCLUIR"]
    
    vector_hallazgos = ["CELULAS ESCAMOSAS NORMALES",
                        "CELULAS GLANDULARES NORMALES",
                        "CAMBIOS CELULARES REACTIVOS A LA INFLAMACIÓN",
        "METAPLASIA ESCAMOSA","METAPLASIA TUBARICA",
        "ALTERACIONES ATRÓFICAS",
        "ALTERACIONES CELULARES SECUNDARIAS A RADIOTERAPIA",
        "ALTERACIONES CELULARES SECUNDARIA A QUIMIOTERAPIA",
        "ALTERACIONES CELULARES SECUNDARIA A DIU",
        "METAPLASIA ESCAMOSA Y CAMBIOS CELULARES REACTIVOS A LA INFLAMACIÓN ",
        "NO INCLUIR"]
    
    vector_cel_escamosas = ["CÉLULAS ESCAMOSAS NORMALES","CÉLULAS ESCAMOSAS ATÍPICAS DE SIGNIFICADO INDETERMINADO (ASC-US)",
        "CÉLULAS ESCAMOSAS ATÍPICAS NO PUEDE EXCLUIRSE LESIÓN DE ALTO GRADO (ASC-H)",
        "LESIÓN INTRAEPITELIAL ESCAMOSA DE BAJO GRADO (L-SIL)",
        "LESIÓN INTRAEPITELIAL ESCAMOSA DE ALTO GRADO (H-SIL)",
        "LESIÓN INTRAEPITELIAL ESCAMOSA DE BAJO GRADO (L-SIL) CON CAMBIOS SUGESTIVOS DE HPV",
        "CARCINOMA EPIDERMOIDE",
        "NO INCLUIR"]
    
    vector_cel_glandulares = ["CÉLULAS GLANDULARES NORMALES","CÉLULAS GLANDULARES ATÍPICAS. (CGA)",
        "CÉLULAS GLANDULARES ATÍPICAS SUGESTIVAS DE NEOPLASIA",
        "ADENOCARCINOMA",
        "NO INCLUIR"]
    
    vector_eval_hormonal = ["PATRON CONCORDANTE CON HISTORIA",
        "TROFICO",
        "HIPOTROFICO",
        "ATROFICO","NO INCLUIR"]
    
    vector_inflamacion = ["LEVE",
        "MODERADA",
        "SEVERA",
        "MODERADA- HEMORRAGICO",
        "SEVERA- HEMORRAGICO",
        "NO INCLUIR"]
    
    vector_conclusion = ["NEGATIVO PARA LESIÓN INTRAEPITELIAL O MALIGNIDAD (NILM)",
        "ANOMALÍA DE CÉLULAS EPITELIALES",
        "POSITIVO PARA LESIÓN INTRAEPITELIAL",
        "POSITIVO PARA NEOPLASIA MALIGNA","NO INCLUIR"]
    
    # vector_opcional = ["combi1","combi2","combi3"]
    vector_lugar = ["La Paz", "El Alto"]
    
    # Lugar_form = Lugar.LUGARES
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
            InformeCitologico.objects.create(CodigoInformeCitologico = cod,
                                             NombresInformeCitologico = nom,
                                             ApellidosInformeCitologico = ape,
                                             EdadInformeCitologico = ed,
                                             MedicoInformeCitologico = med,
                                             HospitalInformeCitologico = hosp,
                                             MuestraInformeCitologico = mues,
                                             DiagnosticoInformeCitologico = diag,
                                             TomaDeMuestraInformeCitologico = fecmues,
                                             RecepcionInformeCitologico = rec,
                                             NumeroDeLaminasInformeCitologico = numlam,
                                             TincionInformeCitologico = tinc, 
                                             EstudioMicroscopicoInformeCitologico=estmic, 
                                             CalidadDeMuestraInformeCitologico=calid,  
                                             MicrorganismosInformeCitologico=micro,
                                             HallazgosInformeCitologico=hall,
                                             CelEscamosasInformeCitologico=esc,
                                             CelGlandularesInformeCitologico=glan,
                                             EvaluacionHormonalInformeCitologico=evalu,
                                             InflamacionInformeCitologico=infla,
                                             ConclusionInformeCitologico=conclu,
                                             RecomendacionInformeCitologico=recomend,
                                             FechaPieInformeCitologico=fech,
                                             LugarInformeCitologico=lug,
                                             DoctorInformeCitologico=doctor)
            
            
            error = "no"
        except:
            error ="yes"
        
        

    d = {'vector_estudio':vector_estudio,
         'vector_calidad':vector_calidad,
         'vector_microorganismos': vector_microorganismos,
         'vector_hallazgos':vector_hallazgos,
         'vector_cel_escamosas':vector_cel_escamosas,
         'vector_cel_glandulares':vector_cel_glandulares,
         'vector_eval_hormonal':vector_eval_hormonal,
         'vector_inflamacion' :vector_inflamacion,
         'vector_conclusion': vector_conclusion,
         'vector_lugar':vector_lugar,
         'doctor':doctor1,'error':error}
    
    return render(request, 'add_informe_cit.html', d)

def Upd_Datos_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCitologico.objects.get(id=pid)

    
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
            paciente.CodigoInformeCitologico=cod
            paciente.NombresInformeCitologico=nom
            paciente.ApellidosInformeCitologico=ape
            paciente.EdadInformeCitologico=ed
            paciente.MedicoInformeCitologico=med
            paciente.HospitalInformeCitologico=hosp
            paciente.MuestraInformeCitologico=mues
            paciente.DiagnosticoInformeCitologico=diag
            paciente.save()
            
            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente}
    return render(request, 'upd_datos_paciente.html', d)

def Upd_Muestra_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCitologico.objects.get(id=pid)

    fecha_muestra = paciente.TomaDeMuestraInformeCitologico.strftime("%Y-%m-%d")
    fecha_recepcion = paciente.RecepcionInformeCitologico.strftime("%Y-%m-%d")
    

    
    if request.method == "POST":
        
        
        fecmues = request.POST['TomaDeMuestra']
        rec = request.POST['Recepcion']
        numlam = request.POST['NumeroDeLaminas']
        tinc = request.POST['Tincion']

        
        try:
            paciente.TomaDeMuestraInformeCitologico=fecmues
            paciente.RecepcionInformeCitologico=rec
            paciente.NumeroDeLaminasInformeCitologico=numlam
            paciente.TincionInformeCitologico=tinc
            paciente.save()
            
            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'fecha_muestra':fecha_muestra,'fecha_recepcion':fecha_recepcion}
    return render(request,'upd_muestra_paciente.html', d)

def Upd_Tabla_Central_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeCitologico.objects.get(id=pid)
    
    vector_estudio = ["EXTENDIDO CITOLÓGICO CONVENCIONAL: EXO-ENDOCERVICAL",
                      "EXTENDIDO CITOLÓGICO POST- HISTERECTOMIA"]
    
    vector_calidad = ["SATISFACTORIO PARA VALORACIÓN CITOLÓGICA: CON PRESENCIA DE CELULAS EPITELIALES DE LA ZONA DE TRANSFORMACIÓN",
        "SATISFACTORIO PARA VALORACIÓN CITOLÓGICA", 
        "INSATISFACTORIO POR AUSENCIA DE CÉLULAS EXOCERVICALES",
        "INSATISFACTORIO POR PRESENCIA DE ESCASAS CÉLULAS EXOCERVICALES",
        "INSATISFACTORIO POR MAS DEL 75% DE CÉLULAS CUBIERTA POR HEMATIES",
        "INSATISFACTORIO POR MAS DEL 75% DE CÉLULAS CUBIERTAS POR INFLAMACIÓN",
        "INSATISFACTORIO POR MAS DEL 75% DE CÉLULAS CUBIERTAS POR HEMATIES E INFLAMACIÓN"]
    
    vector_microorganismos = ["FLORA HABITUAL","FLORA BACTERIANA MIXTA",
        "FLORA COCOIDE","CAMBIOS EN LA FLORA SUGESTIVOS DE VAGINOSIS BACTERIANA",       
        "TRICHOMONAS VAGINALIS","ORGANISMOS MICÓTICOS MORFOLOGICAMENTE COMPATIBLES CON CANDIDA SP",
        "BACTERIAS MORFOLOGICAMENTE COMPATIBLES CON ACTYNOMICES SP",
        "CAMBIOS COMPATIBLES CON VIRUS HERPES SIMPLE",
        "NO INCLUIR"]
    
    vector_hallazgos = ["CELULAS ESCAMOSAS NORMALES",
                        "CELULAS GLANDULARES NORMALES",
                        "CAMBIOS CELULARES REACTIVOS A LA INFLAMACIÓN",
        "METAPLASIA ESCAMOSA","METAPLASIA TUBARICA",
        "ALTERACIONES ATRÓFICAS",
        "ALTERACIONES CELULARES SECUNDARIAS A RADIOTERAPIA",
        "ALTERACIONES CELULARES SECUNDARIA A QUIMIOTERAPIA",
        "ALTERACIONES CELULARES SECUNDARIA A DIU",
        "METAPLASIA ESCAMOSA Y CAMBIOS CELULARES REACTIVOS A LA INFLAMACIÓN ",
        "NO INCLUIR"]
    
    vector_cel_escamosas = ["CÉLULAS ESCAMOSAS NORMALES","CÉLULAS ESCAMOSAS ATÍPICAS DE SIGNIFICADO INDETERMINADO (ASC-US)",
        "CÉLULAS ESCAMOSAS ATÍPICAS NO PUEDE EXCLUIRSE LESIÓN DE ALTO GRADO (ASC-H)",
        "LESIÓN INTRAEPITELIAL ESCAMOSA DE BAJO GRADO (L-SIL)",
        "LESIÓN INTRAEPITELIAL ESCAMOSA DE ALTO GRADO (H-SIL)",
        "LESIÓN INTRAEPITELIAL ESCAMOSA DE BAJO GRADO (L-SIL) CON CAMBIOS SUGESTIVOS DE HPV",
        "CARCINOMA EPIDERMOIDE",
        "NO INCLUIR"]
    
    vector_cel_glandulares = ["CÉLULAS GLANDULARES NORMALES","CÉLULAS GLANDULARES ATÍPICAS. (CGA)",
        "CÉLULAS GLANDULARES ATÍPICAS SUGESTIVAS DE NEOPLASIA",
        "ADENOCARCINOMA",
        "NO INCLUIR"]
    
    vector_eval_hormonal = ["PATRON CONCORDANTE CON HISTORIA",
        "TROFICO",
        "HIPOTROFICO",
        "ATROFICO","NO INCLUIR"]
    
    vector_inflamacion = ["LEVE",
        "MODERADA",
        "SEVERA",
        "MODERADA- HEMORRAGICO",
        "SEVERA- HEMORRAGICO",
        "NO INCLUIR"]
    
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
            paciente.EstudioMicroscopicoInformeCitologico=estmic
            paciente.CalidadDeMuestraInformeCitologico= calid
            paciente.MicrorganismosInformeCitologico= micro
            paciente.HallazgosInformeCitologico= hall
            paciente.CelEscamosasInformeCitologico= esc
            paciente.CelGlandularesInformeCitologico= glan
            paciente.EvaluacionHormonalInformeCitologico= evalu
            paciente.InflamacionInformeCitologico= infla
            paciente.save()

            
            error = "no"
        except:
            error ="yes"

    d = {'error':error,
         'paciente':paciente,
         'vector_estudio':vector_estudio,
         'vector_calidad':vector_calidad,
         'vector_microorganismos': vector_microorganismos,
         'vector_hallazgos':vector_hallazgos,
         'vector_cel_escamosas':vector_cel_escamosas,
         'vector_cel_glandulares':vector_cel_glandulares,
         'vector_eval_hormonal':vector_eval_hormonal,
         'vector_inflamacion' :vector_inflamacion}
    
    return render(request,'upd_tabla_central_paciente.html', d)

def Upd_Conclusion_Paciente(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    vector_conclusion = ["NEGATIVO PARA LESIÓN INTRAEPITELIAL O MALIGNIDAD (NILM)",
        "ANOMALÍA DE CÉLULAS EPITELIALES",
        "POSITIVO PARA LESIÓN INTRAEPITELIAL",
        "POSITIVO PARA NEOPLASIA MALIGNA","NO INCLUIR"]
    
    
    vector_lugar = ["La Paz", "El Alto"]
    
    paciente = InformeCitologico.objects.get(id=pid)

   
    fecha_informe = paciente.FechaPieInformeCitologico.strftime("%Y-%m-%d")
    
    
    
    if request.method == "POST":
        
        conclu = request.POST['Conclusion']
        recomend = request.POST['Recomendacion']
        fech = request.POST['FechaPie']
        lug = request.POST['Lugar']
        # combi = 'opcion1'
        
        try:
            paciente.ConclusionInformeCitologico = conclu
            paciente.RecomendacionInformeCitologico = recomend
            paciente.FechaPieInformeCitologico = fech
            paciente.LugarInformeCitologico = lug
            
            paciente.save()

            

            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'vector_conclusion':vector_conclusion,'lugar':vector_lugar,'fechainf':fecha_informe}
    return render(request,'upd_conclusion_paciente.html', d)

def Delete_Informe_Cit(request,pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    informeCit = InformeCitologico.objects.get(id=pid)
    
    
    informeCit.delete()
    

    return redirect('view_informe')

def Add_Informe_Anat(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    
    doctor1=Doctor.objects.all()

    vectorMacros = ["Amígdalas","Apéndices","Leiomioma","Placenta",
                    "Biopsias gástricas","Restos Ovulares","Próstata","Utero",
                    "Vesícula"]
    vectorMicros = ["Apéndice","Vesícula","Próstata","Aborto"]
    vector_lugar = ["La Paz", "El Alto"]
    
    if request.method == "POST":
        
        cod=request.POST['Codigo']
        
        nom = request.POST['Nombres']
        ape = request.POST['Apellidos']
        ed = request.POST['Edad']
        med = request.POST['Medico']
        hosp = request.POST['Hospital']
        mues = request.POST['Muestra']
        diag = request.POST['Diagnostico']  
        
        
        rec = request.POST['Recepcion']
          
        estmicro = request.POST['MicroResultado']
        estmacro = request.POST['MacroResultado']
        especimen = request.POST['Especimen']
        conclusion = request.POST['Conclusion']     
        fech = request.POST['FechaPie']
        lug = request.POST['Lugar'] 
        
        n = request.POST['doctor']  
        doctor=Doctor.objects.filter(Name=n).first()    
         
        try:
            InformeAnatomico.objects.create(CodigoInformeAnatomico = cod,
                                            NombresInformeAnatomico = nom,
                                            ApellidosInformeAnatomico = ape,
                                            EdadInformeAnatomico = ed,
                                            MedicoInformeAnatomico = med,
                                            HospitalInformeAnatomico = hosp,
                                            MuestraInformeAnatomico = mues,
                                            DiagnosticoInformeAnatomico = diag,
                                            RecepcionInformeAnatomico = rec,
                                            EstudioMacroscopicoInformeAnatomico=estmacro,
                                            EstudioMicroscopicoInformeAnatomico=estmicro,
                                            EspecimenInformeAnatomico = especimen,
                                            ConclusionInformeAnatomico = conclusion,
                                            FechaPieInformeAnatomico = fech,
                                            LugarInformeAnatomico = lug,
                                            DoctorInformeAnatomico = doctor)
            error = "no"
        except:
            error ="yes"    

    d = {'error':error,'vector':vectorMicros,'vectorMacros':vectorMacros,'lugar':vector_lugar,'doctor':doctor1}

    return render(request, 'add_informe_anat.html', d)

def micros2(request):
    micros1 = request.GET.get('micros1')

    vApendice = ["A.01","A.02","A.1","A.2","A.3","A.4","A.5","A.6","A.7","A.80","A.81"]
    vVesicula = ["V.0 COLECISTITIS AGUDA","V.1 COLECISTITIS AGUDA",
                 "V.2 COLECISTITIS AGUDA","V.3 COLECISTITIS AGUDA Y PERICOLECISTITIS",
                 "V.4 COLECISTITIS AGUDA MAS LINFOADENITIS",
                 "V.5 COLECISTITIS CRONICA REAGUDIZADA MAS GANGLIO",
                 "V.6 COLECISTITIS CRONICA SUBAGUDA",
                 "V.8 COLECISTITIS CRONICA REAGUDIZADA",
                 "V.9 COLECISITIS CRONICA REAGUDIZADA",
                 "V.10 COLECISTITIS CRONICA",
                 "V.11 COLECISTITIS CRONICA",
                 "COLECISTITIS CRONICA MAS ADENOMIOSIS",
                 "V.12 COLELITIASIS  MAS COLECISTITIS CRONICA MAS LINFOADENITIS",
                 "V.13 COLELITIASIS-CC-POLIPO COLESTERINICO",
                 "V.14 CCL-COLESTEROLOSIS"
                 "V.14_1",
                 "COLECISTITIS CRONICA RA MAS COLESTEROLOSIS",
                 "V.15 CCL MAS POLIPOS COLESTERINICOS",
                 "V.16 CCRA MAS POLIPOS COLESTERINICOS",
                 "CC MAS METAPLASIA INTESTINAL",
                 "CANCER DE VESICULA",
                 "CANCER DE VESICULA 1",
                 "CANCER DE VESICULA 2",
                 "CANCER DE VESICULA 3"]
    vProstata = ["ADENECTOMIA PROSTATA","BIOPSIAS DE PROSTATA CON RADIOTERAPIA",
                 "MAPEO","MAPEO PROSTATICO","RTU DE PROSTATA"," MAPEO PROSTATICO 1",
                 "RTU DE PROSTATA 1","RTU DE PROSTATA 2",
                 "ADENECTOMIA CON FOCOS DE INFARTO ANTIGUO",
                 "MAPEO CON ADENOCARCINOMA EN TODAS LAS MUESTRAS",
                 "RTU CON CANCER"]
    vAborto = ["RESTOS PRIMER TRIMESTRE","RESTOS PRIMER TRIMESTRE 1",
               "ENDOMETRIO CON CAMBIOS DECIDUOIDES","MOLA PARCIAL"]

    if micros1 == 'Apéndice':
        vector1 = vApendice
    elif micros1 == 'Vesícula':
        vector1 = vVesicula
    elif micros1 == 'Próstata':
        vector1 = vProstata
    elif micros1 == 'Aborto':
        vector1 = vAborto
    
    context = {'vector1': vector1,'viene':micros1}
    
    return render(request, 'micros2.html', context)

def micros3(request):
    valueToSend = 'pas encore'
    micros2 = request.GET.get('micros2')

    if micros2 == 'A.01':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa apendicular  con cambios congestivos, edema y una hiperplasia de centros germinales a nivel de la lámina propia. La serosa ofrece congestión.'
    elif micros2 == 'A.02':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa apendicular  con cambios caracterizados por   áreas de edema focal, hiperplasia de folículos linfoides  y vasos dilatados. '
    elif micros2 == 'A.1':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa apendicular  con un proceso inflamatorio agudo caracterizado por   áreas de edema, hiperplasia de folículos linfoides, necrosis focal del epitelio   y vasos dilatados.'
    elif micros2 == 'A.2':
        valueToSend = 'Pared y mucosa apendicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema, necrosis focal y hemorragia.  La serosa ofrece congestión.'
    elif micros2 == 'A.3':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa apendicular  con un proceso inflamatorio agudo caracterizado por extensas  áreas de edema, necrosis  y hemorragia.'
    elif micros2 == 'A.4':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa apendicular  con un proceso inflamatorio agudo caracterizado por extensas  áreas de edema, necrosis  y hemorragia.  La serosa ofrece congestión.'
    elif micros2 == 'A.5':
        valueToSend = 'Pared  y  mucosa apendicular  con un proceso inflamatorio agudo caracterizado por  extensas áreas de necrosis, infiltrados inflamatorios de tipo polimorfonuclear y hemorragia.   Dicho proceso se extiende focalmente  hasta la serosa vecina.'
    elif micros2 == 'A.6':
        valueToSend = 'Pared y mucosa apendicular con un proceso inflamatorio agudo caracterizado por extensas áreas de necrosis, infiltrados inflamatorios de tipo polimorfonuclear y hemorragia.   Dicho proceso se extiende focalmente  hasta la serosa vecina.'
    elif micros2 == 'A.7':
        valueToSend = 'Pared y mucosa apendicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema, necrosis, infiltrados inflamatorios de tipo polimorfonuclear y hemorragia.  Dicho proceso se extiende hasta la serosa vecina.'
    elif micros2 == 'A.80':
        valueToSend = 'Pared y mucosa apendicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema, necrosis y hemorragia.  Dicho proceso se extiende hasta la serosa  y meso vecino.'
    elif micros2 == 'A.81':
        valueToSend = 'El estudio histológico  evidencia: 	\n 1.-	Pared y mucosa apendicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema, necrosis y hemorragia.  Dicho proceso se extiende hasta la serosa  y meso vecino. \n 2.- Tejido adiposo con áreas de edema, hemorragia, infiltrados inflamatorios de tipo agudo y necrosis.'
    
    elif micros2 == 'V.0 COLECISTITIS AGUDA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema, necrosis, infiltrados inflamatorios de tipo polimorfonuclear y áreas de hemorragia.  El epitelio muestra áreas de erosión y la serosa ofrece congestión.'
    elif micros2 == 'V.1 COLECISTITIS AGUDA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema,  necrosis y hemorragia.  Dicho proceso se extiende hasta la serosa vecina.'
    elif micros2 == 'V.2 COLECISTITIS AGUDA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico subagudo caracterizado infiltrados inflamatorios de tipo mixto con  proliferación fibroblástica, congestión vascular,  focos de edema y erosión focal del epitelio.'
    elif micros2 == 'V.3 COLECISTITIS AGUDA Y PERICOLECISTITIS':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio agudo caracterizado por extensas áreas de edema,  necrosis y hemorragia.  El epitelio muestra erosión y necrosis. Dicho proceso se extiende hasta la serosa vecina.'
    elif micros2 == 'V.4 COLECISTITIS AGUDA MAS LINFOADENITIS':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio agudo caracterizado por infiltrados inflamatorios de tipo polimorfonuclear, áreas de edema, hemorragia y vasos dilatados.  El epitelio es normotípico y la serosa ofrece congestión. Los cortes del ganglio muestran senos dilatados y centros germinales hiperplásicos.'
    elif micros2 == 'V.5 COLECISTITIS CRONICA REAGUDIZADA MAS GANGLIO':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico reagudizado  con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y polimorfonuclear así como  vasos dilatados.  El epitelio es normotípico y la serosa ofrece congestión. Los cortes del ganglio muestran senos dilatados y centros germinales hiperplásicos.'
    elif micros2 == 'V.6 COLECISTITIS CRONICA SUBAGUDA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio subagudo caracterizado por áreas de edema, hemorragia, erosión focal del epitelio e infiltrados inflamatorios de tipo mixto. La serosa ofrece congestión.'
    elif micros2 == 'V.8 COLECISTITIS CRONICA REAGUDIZADA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico reagudizado caracterizado por extensas áreas de edema, hemorragia, infiltrados inflamatorios de tipo mixto y congestión.  El epitelio muestra erosión y la serosa ofrece congestión.'
    elif micros2 == 'V.9 COLECISITIS CRONICA REAGUDIZADA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico reagudizado caracterizado por extensas áreas de edema, hemorragia, infiltrados inflamatorios de tipo mixto y congestión.  El epitelio muestra erosión y la serosa ofrece congestión.'
    elif micros2 == 'V.10 COLECISTITIS CRONICA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y vasos dilatados.  El epitelio es normotípico y la serosa ofrece congestión.'
    elif micros2 == 'V.11 COLECISTITIS CRONICA':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y vasos dilatados.  El epitelio es normotípico y la serosa ofrece congestión.'
    elif micros2 == 'COLECISTITIS CRONICA MAS ADENOMIOSIS':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa vesicular con un proceso inflamatorio crónico con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y vasos dilatados.  El epitelio es normotípico  con invaginaciones hacia la muscular con focos de dilatación quística.  La serosa ofrece congestión.'
    elif micros2 == 'V.12 COLELITIASIS  MAS COLECISTITIS CRONICA MAS LINFOADENITIS':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y vasos dilatados.  El epitelio es normotípico y la serosa ofrece congestión. Los cortes del ganglio muestran senos dilatados y centros germinales hiperplásicos.'
    elif micros2 == 'V.13 COLELITIASIS-CC-POLIPO COLESTERINICO':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y vasos dilatados.  El epitelio es normotípico y ofrece una formación polipoide  en cuyo estroma se identifican histiocitos de citoplasma espumoso. La serosa ofrece congestión.'
    elif micros2 == 'V.14 CCL-COLESTEROLOSIS':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico   caracterizado por infiltrados inflamatorios de tipo linfoplasmocitario  con áreas de fibrosis y  vasos engrosados.   El epitelio es normotípico y muestra áreas de erosión  y a nivel de la lámina propia se identifican histiocitos de citoplasma espumoso.'
    elif micros2 == 'V.14_1':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico caracterizado por infiltrados inflamatorios de tipo linfoplasmocitario  con áreas de fibrosis y  vasos engrosados.   El epitelio es normotípico y muestra áreas de erosión  y a nivel de la lámina propia se identifican histiocitos de citoplasma espumoso. Uno de los cortes muestra un ganglio con cambios reactivos.'
    elif micros2 == 'COLECISTITIS CRONICA RA MAS COLESTEROLOSIS':
        valueToSend = 'El estudio histológico  evidencia: Pared y mucosa vesicular con un proceso inflamatorio crónico reagudizado con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y polimorfonuclear así como vasos dilatados.  El epitelio es normotípico y ofrece a nivel del estroma histiocitos de citoplasma espumoso. La serosa ofrece congestión.'
    elif micros2 == 'V.15 CCL MAS POLIPOS COLESTERINICOS':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y vasos dilatados.  El epitelio es normotípico y ofrece múltiples  formaciones polipoides  en cuyo estroma se identifican histiocitos de citoplasma espumoso. La serosa ofrece congestión.'
    elif micros2 == 'V.16 CCRA MAS POLIPOS COLESTERINICOS':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico reagudizado con áreas de fibrosis, infiltrados inflamatorios de tipo linfoplasmocitario y polimorfonuclear así como vasos dilatados.  El epitelio es normotípico y ofrece múltiples  formaciones polipoides  en cuyo estroma se identifican histiocitos de citoplasma espumoso. La serosa ofrece congestión.'
    elif micros2 == 'CC MAS METAPLASIA INTESTINAL':
        valueToSend = 'Pared y mucosa vesicular con un proceso inflamatorio crónico caracterizado por áreas de fibrosis, hialinización y hemorragia.  El epitelio  muestra una extensa metaplasia intestinal y focos con células de  núcleos aumentados de tamaño, cromatina granular,  nucleolo prominente, escaso citoplasma, algunas figuras de mitosis y moderada pérdida de la polaridad.'
    elif micros2 == 'CANCER DE VESICULA':
        valueToSend = 'El estudio histológico  evidencia : 	Pared y mucosa vesicular con un adenocarcinoma moderadamente diferenciado e infiltrante conformado por células de núcleos pleomórficos con nucléolo prominente y escaso citoplasma dispuestas en estructuras pseudoglandulares que infiltran el estroma vecino llegando hasta la subserosa. Existe permeación perineural y vascular.'
    elif micros2 == 'CANCER DE VESICULA 1':
        valueToSend = 'El estudio histológico  evidencia: Pared y mucosa vesicular con un proceso inflamatorio crónico y reagudizado caracterizado por áreas de fibrosis, hialinización y hemorragia.  El epitelio  muestra una extensa metaplasia intestinal y focos con células de  núcleos aumentados de tamaño, cromatina granular,  nucléolo prominente, escaso citoplasma, algunas figuras de mitosis y moderada pérdida de la polaridad. Dichas células infiltran focalmente la lámina propia.'
    elif micros2 == 'CANCER DE VESICULA 2':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa vesicular con un proceso inflamatorio crónico con extensas áreas de fibrosis y calcificación además de infiltrados inflamatorios de tipo linfoplasmocitario. El epitelio se halla esfacelado.'
    elif micros2 == 'CANCER DE VESICULA 3':
        valueToSend = 'El estudio histológico  evidencia: 	Pared y mucosa vesicular infiltradas por una neoplasia conformada por células de núcleos aumentados de tamaño con una cromatina irregular, nucléolo prominente, escaso citoplasma y figuras de mitosis atípicas. Dichas células se disponen en mantos sobre un estroma con áreas de necrosis, hemorragia y edema y se  extienden hasta la subserosa.'

    elif micros2 == 'ADENECTOMIA PROSTATA':
        valueToSend = 'Tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma.  El estroma  es de tipo fibromuscular y muestra áreas de edema, hemorragia y congestión. '
    elif micros2 == 'BIOPSIAS DE PROSTATA CON RADIOTERAPIA':
        valueToSend = '1 y 2.-  Fragmentos de tejido prostático con una reducida población de alveolos disminuidos de tamaños revestidos por  un epitelio de núcleos basales hipercromáticos, moderado citoplasma y una población de células basaloides con cambios reactivos.  El estroma  es de tipo fibromuscular con leve congestión.'
    elif micros2 == 'MAPEO':
        valueToSend = 'El estudio histológico  evidencia: Fragmentos de tejido prostático con la presencia de estructuras glandulares disminuidas de tamaño revestidas por un epitelio de núcleos aumentados de tamaño con nucléolo prominente y escaso citoplasma. Dichas estructuras están rodeadas por fibrosis y hialinización.'
    elif micros2 == 'MAPEO PROSTATICO':
        valueToSend = 'Fragmentos de tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma.  El estroma  es de tipo fibromuscular y muestra áreas de edema, hemorragia y congestión.'
    elif micros2 == 'RTU DE PROSTATA':
        valueToSend = 'Fragmentos de tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma.  El estroma  es de tipo fibromuscular y muestra áreas de edema, hemorragia, fibrosis, hialinización y congestión.'
    elif micros2 == 'MAPEO PROSTATICO 1':
        valueToSend = 'Fragmentos de tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma.  El estroma  es de tipo fibromuscular y muestra áreas de edema, hemorragia, densos infiltrados inflamatorios de tipo mixto y congestión.'
    elif micros2 == 'RTU DE PROSTATA 1':
        valueToSend = 'Fragmentos de tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma.  El estroma  es de tipo fibromuscular, áreas de edema, hemorragia e infiltrados inflamatorios de tipo agudo  y crónico. '
    elif micros2 == 'RTU DE PROSTATA 2':
        valueToSend = 'Fragmentos de tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma rodeados por infiltrados inflamatorios de tipo agudo con focos de necrosis intraluminal.  El estroma  es de tipo fibromuscular con áreas de edema, hemorragia y congestión.'
    elif micros2 == 'ADENECTOMIA CON FOCOS DE INFARTO ANTIGUO':
        valueToSend = 'Tejido prostático con alveolos de tamaños variables revestidos por  un epitelio de núcleos basales y moderado citoplasma.  El estroma  es de tipo fibromuscular y muestra áreas de edema, hemorragia y congestión.  Existen focos con áreas de infarto antiguo rodeadas por fibrosis y hialinización.'
    elif micros2 == 'MAPEO CON ADENOCARCINOMA EN TODAS LAS MUESTRAS':
        valueToSend = 'Fragmentos de tejido prostático con la presencia de estructuras glandulares disminuidas de tamaño revestidas por un epitelio de núcleos aumentados de tamaño con nucleolo prominente y escaso citoplasma. Dichas estructuras presentan un patrón irregular e infiltrante y están rodeadas por fibrosis y hialinización.'
    elif micros2 == 'RTU CON CANCER':
        valueToSend = 'Fragmentos de tejido prostático con la presencia de estructuras glandulares disminuidas de tamaño revestidas por un epitelio de núcleos aumentados de tamaño con nucléolo prominente y escaso citoplasma. Dichas estructuras presentan un patrón irregular e infiltrante y están rodeadas por fibrosis y hialinización.'
        
    elif micros2 == 'RESTOS PRIMER TRIMESTRE':
        valueToSend = 'El estudio histológico  evidencia: 	Vellosidades coriales del primer trimestre de gestación con cambios involutivos caracterizados por un estroma laxo con vasos dilatados y presencia de glóbulos rojos fetales. El trofoblasto muestra proliferación focal. Dichas estructuras están entremezcladas con fragmentos deciduales y material fibrinohemático.'
    elif micros2 == 'RESTOS PRIMER TRIMESTRE 1':
        valueToSend = 'El estudio histológico  evidencia: 	Vellosidades coriales del primer trimestre de gestación con cambios involutivos caracterizados por un estroma laxo con vasos dilatados y calcificación. Dichas estructuras están entremezcladas con material fibrinohemático y endometrio de tipo secretor con inflamación.'
    elif micros2 == 'ENDOMETRIO CON CAMBIOS DECIDUOIDES':
        valueToSend = 'l estudio histológico  evidencia: Fragmentos de endometrio con glándulas de diferentes tamaños revestidas por un epitelio columnar simple secretor, con células de núcleos basales y amplio citoplasma. El estroma muestra extensas áreas con cambios deciduoides, edema, congestión y hemorragia. Dichas estructuras están entremezcladas con  material fibrinohemático.'
    elif micros2 == 'MOLA PARCIAL':
        valueToSend = 'El estudio histológico  evidencia: Vellosidades coriales aumentadas de tamaño con un estroma amplio, laxo y vesiculoso, con proliferación del cito y sincitiotrofoblasto. Dichas Estructuras están entremezcladas con material fibrinohemático y endometrio de tipo hipersecretor.'

    context = {'sent':valueToSend}
    return render(request, 'micros3.html', context)

def macros2(request):
    
    macros1 = request.GET.get('macros1')
    vAmigdalas = ["AMIGDALAS EN DOS FRASCOS","AMIGDALAS EN UN FRASCO",
                   "AMIGDALAS MAS ADENOIDES EN TRES FRASCOS",
                   "ADENOIDES"]
    vApendices = ["APENDICITIS AGUDA FIBRINOSA",
                   "APENDICITIS AGUDA EN FASE CONGESTIVA",
                   "APENDICE FRAGMENTADO","OPCION 4"]
    vLeiomioma = ["OPCION1","MIOMAS"]
    vPlacenta = ["OPCION1"]
    vBiopsiasGastricas = ["BIOPSIA GASTRICA UN FRAGMENTO",
                          "BIOPSIAS GASTRICAS  FRAGMENTOS",
                          "BIOPSIAS GASTRICAS  FRAGMENTOS ENUMERADOS"]
    vRestosOvulares = ["RESTOS OVULARES 1","RESTOS OVULARES 2",
                       "RESTOS OVULARES 3"]
    vProstata = ["PROSTATA BILOBULADA; PIEZA OPERATORIA",
                 "PROSTATA TRILOBULADA; PIEZA OPERATORIA",
                 "MUESTRAS DE PROSTATA",
                 "RTU DE PROSTATA",
                 "MAPEO DE PROSTATA",
                 "MAPEO DE PROSTATA 2",
                 "MAPEO PROSTATICO CON SEIS FRASCOS"]
    vUtero = ["UTERO SIN ANEXOS","UTERO SIN ANEXOS MAS MIOMAS",
              "UTERO CON  ANEXOS","UTERO CON  ANEXOS MAS MIOMAS"]
    vVesicula = ["COLECISTITIS CRONICA","COLECISTITIS CRONICA LITIASICA",
                 "COLECISTITIS CRONICA LITIASICA MAS GANGLIO",
                 "COLECISTITIS CRONICA COLESTEROLOSICA",
                 "COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA",
                 "COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA MAS GANGLIO CISTICO",
                 "COLECISTITIS CRONICA ESCLEROSANTE",
                 "COLECISTITIS CRONICA ESCLEROSANTE LITIASICA",
                 "COLECISTITIS AGUDA",
                 "COLECISTITIS AGUDA LITIASICA",
                 "COLECISTITIS AGUDA LITIASICA MAS GANGLIO CISTICO",
                 "VB CERRADA COLECISTITIS CRONICA",
                 "VB CERRADA COLECISTITIS CRONICA LITIASICA",
                 "VB CERRADA COLECISTITIS CRONICA LITIASICA MAS GANGLIO",
                 "VB CERRADA COLECISTITIS CRONICA COLESTEROLOSICA",
                 "VB CERRADA COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA",
                 "VB CERRADA COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA MAS GANGLIO CISTICO",
                 "VB CERRADA COLECISTITIS AGUDA",
                 "VB CERRADA COLECISTITIS AGUDA LITIASICA",
                 "VB CERRADA COLECISTITIS AGUDA LITIASICA MAS GANGLIO CISTICO",
                 "VB FRAGMENTADA COLECISTITIS CRONICA",
                 "VB FRAGMENTADA COLECISTITIS CRONICA LITIASICA",
                 "VB FRAGMENTADA COLECISTITIS CRONICA LITIASICA MAS GANGLIO",
                 "VB FRAGMENTADA COLECISTITIS CRONICA COLESTEROLOSICA",
                 "VB FRAGMENTADA COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA"
                 "VB FRAGMENTADA COLECISTITIS AGUDA",
                 "VB FRAGMENTADA COLECISTITIS AGUDA LITIASICA"]

    
    if macros1 == 'Amígdalas':
        vector1 = vAmigdalas
    elif macros1 == 'Apéndices':
        vector1 = vApendices
    elif macros1 == 'Leiomioma':
        vector1 = vLeiomioma
    elif macros1 == 'Placenta':
        vector1 = vPlacenta
    elif macros1 == 'Biopsias gástricas':
        vector1 = vBiopsiasGastricas
    elif macros1 == 'Restos Ovulares':
        vector1 = vRestosOvulares
    elif macros1 == 'Próstata':
        vector1 = vProstata
    elif macros1 == 'Utero':
        vector1 = vUtero
    elif macros1 == 'Vesícula':
        vector1 = vVesicula

    context = {'vector1': vector1,'viene':macros1}
    return render(request, 'macros2.html', context)

def macros3(request):
    
    valueToSend = 'pas encore'
    macros2 = request.GET.get('macros2')

    if macros2 == 'AMIGDALAS EN DOS FRASCOS':
        valueToSend = 'Se reciben dos frascos: \n 1.- Identificado como “amígdala derecha”, contiene una muestra tisular irregularmente ovoidea que 2.3 x 1.8 x 1.2 cm. y pesa 3 gr., presenta una superficie  blanco-grisácea y críptica y otra superficie irregular y pardo-grisácea. Al corte sus caras  de sección son blanco-grisáceas y heterogéneas. Se incluyen cortes representativos. \n 2.- Identificado como “amígdala izquierda”, contiene una muestra tisular irregularmente ovoidea que 3.3 x 2 x 1.8 cm. y pesa 6 gr., presenta una superficie  blanco-grisácea y críptica y otra superficie irregular y pardo-grisácea. Al corte sus caras  de sección son blanco-grisáceas y heterogéneas. Se incluyen cortes representativos.'
    elif macros2 == 'AMIGDALAS EN UN FRASCO':
        valueToSend ='Se recibe un frasco con dos muestras tisulares irregularmente ovoideas y blandas que miden entre 3 x 2.2 x 1.7 y 2.8 x 1.9 x 1.5 cm., pesan 6 y 5 gr. respectivamente, presentan una superficie blanco-grisácea críptica y otra anfractuosa, irregular y pardo-grisácea. Al corte sus caras de sección son heterogéneas y blanco-grisáceas. Se incluyen  cortes representativos.'
    elif macros2 == 'AMIGDALAS MAS ADENOIDES EN TRES FRASCOS':
        valueToSend = 'Se reciben tres frascos: \n 1.- Identificado como “tonsila derecha”, contiene una muestra tisular irregularmente ovoidea que mide 3.2 x 2 x 1.5 cm.  y pesa 4 gr., presenta una superficie  blanco-grisácea y críptica y otra superficie irregular y pardo-grisácea. Al corte sus caras  de sección son blanco-grisáceas y heterogéneas. Se incluyen cortes representativos. \n 2.- Identificado como “tonsila izquierda”, contiene una muestra tisular irregularmente ovoidea que mide 3 x 2 x 1.5 cm.  y pesa 4 gr., presenta una superficie  blanco-grisácea y críptica y otra superficie irregular y pardo-grisácea. Al corte sus caras  de sección son blanco-grisáceas y heterogéneas. Se incluyen cortes representativos.\n 3.- Identificado como “tonsila faríngea”, contiene una gasa con tres fragmentos tisulares irregulares, blandos y blanco-grisáceos que miden entre 0.7 y 1.2 cm.  y que en conjunto pesan 1 gr., con una superficie finamente granular y de consistencia blanda. Se incluyen en su totalidad.'
    elif macros2 == 'ADENOIDES':
        valueToSend = 'Son  varios fragmentos tisulares irregulares, blandos y pardo-grisáceos que miden entre 00.0 y 00.0 cm. de longitud x 00.0 y 00.0 cm de ancho x 00.0 y 00.0 cm de espesor y que en conjunto pesan 00.0 gr., con una superficie finamente granular y de consistencia blanda. Se incluyen en su totalidad.'
    
    elif macros2 == 'APENDICITIS AGUDA FIBRINOSA':
        valueToSend = 'Apéndice cecal que mide  8.5 cm. de longitud x 1 cm. de diámetro mayor, su serosa es pardo-grisácea con placas de fibrina. Al corte su pared mide 0.3 cm. de espesor y su mucosa es pardo-grisácea  con material fecaloide y hemático en su luz además de un coprolito a nivel de su tercio medio. Se incluyen cortes representativos.'
    elif macros2 == 'APENDICITIS AGUDA EN FASE CONGESTIVA':
        valueToSend = 'Apéndice cecal que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es blanco-grisácea con vasos congestivos. Al corte su pared mide 00.0 cm. de espesor, su mucosa es congestiva con material fecaloide en su luz. Se incluyen cortes representativos.'
    elif macros2 == 'APENDICE FRAGMENTADO':
        valueToSend = 'Apéndice cecal fragmentado en dos segmentos que en conjunto mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es pardo-grisácea con placas de fibrina. Al corte su pared mide 0 cm. de espesor y su mucosa es pardo-grisácea con material fecaloide y hemático en su luz además de un coprolito a nivel del tercio medio. Se incluyen cortes representativos.'
    elif macros2 == 'OPCION 4':
        valueToSend = 'Apéndice cecal plastronado que mide  5 cm. de longitud x 1 cm. de diámetro mayor, su serosa es pardo-oscura con vasos congestivos y areas hemorragicas. Al corte su pared mide 0.3 cm. de espesor y  material fecaloide en su luz. Adjunto muestra irregular de tejido adiposo, pardo- amarillento que mide 5 x 3 x 1cm; al corte pardo amarillento con areas congestivas y hemorragicas.  Se incluyen cortes representativos.'
    
    #LEIOMIOMA
    elif macros2 == 'OPCION1':
        valueToSend = 'Se recibe una masa aumentada de consistencia que mide 11 x 8 x 7 cm. y que pesa 301 gr. su superficie es lisa y blanco-parduzca con áreas irregulares y nodulares. Al corte sus caras de sección son heterogéneas y blanco-grisáceas con haces de aspecto arremolinado. Se incluyen cortes representativos. '
    elif macros2 == 'MIOMAS':
        valueToSend = 'Se reciben cuatro muestras tisulares nodulares aumentadas de consistencia que miden entre 6.5 x 6.2 x 5.4 y 1.6 x 1.2 x 1. cm. y que en conjunto pesan 161 gr. sus superficies son lisas y blanco-parduzcas con áreas nodulares. Al cortes sus caras de sección son  heterogéneas y blanco-grisáceas con haces de aspecto arremolinado. Se incluyen cortes representativos.'

    #PLACENTA

    elif macros2 == 'OPCION1':
        valueToSend = 'Se recibe placenta que mide 18.5 x 15.5 cm.de diámetros x 3.8 cm. de espesor, pesa 372 gr., su cara fetal es lisa y blanco-grisácea con inserción marginal de segmento de cordón umbilical que mide 25.5 cm. de longitud x 1.5 cm. de diámetro mayor, que al corte muestra tres luces vasculares. Las membranas son elásticas, traslúcidas y parduzcas de inserción circunmarginal. La cara materna es irregular con cotiledones esfacelados e irregulares que presentan algunas formaciones blanco-grisáceas en sus superficies, al corte sus caras de sección son heterogéneas, pardo-rojizas de aspecto esponjoso.  Se incluyen cortes representativos. '
    
    #BIOPIAS GASTRICAS

    elif macros2 == 'BIOPSIA GASTRICA UN FRAGMENTO':
        valueToSend = 'Biopsia identificada como proveniente de estómago que consiste en un fragmento tisular irregular, blando y blanco-grisáceo que mide 0.3 x 0.2 x 0.1  cm. íntegramente incluido.'
    elif macros2 == 'BIOPSIAS GASTRICAS  FRAGMENTOS':
        valueToSend = 'Biopsias identificadas como provenientes de estómago que consisten en dos fragmentos tisulares irregulares, blandos y blanco-grisáceos que miden entre 0.3 x 0.3 x 0.2 y 0.3 x 0.2 x 0.1 cm. íntegramente incluidos.'
    elif macros2 == 'BIOPSIAS GASTRICAS  FRAGMENTOS ENUMERADOS':
        valueToSend = 'Biopsias identificadas como provenientes de estómago que consisten en cinco fragmentos tisulares irregulares, blandos y blanco-grisáceos que miden entre 0.3 x 0.2 x 0.1 y 0.2 x 0.2 x 0.1 cm. enumerados del 1 al 5, las muestras son  íntegramente incluidas según señalización.'
    
    #RESTOS OVULARES
    
    elif macros2 == 'RESTOS OVULARES 1':
        valueToSend = 'Se reciben varios fragmentos tisulares irregulares, blandos, desflecados y pardo-grisáceos de aspecto membranoso y esponjoso que miden entre 0.3 y 1.2 cm. y que  en conjunto pesan 9 grs., entremezclados con material hemático, íntegramente incluidos.'
    elif macros2 == 'RESTOS OVULARES 2':
        valueToSend = 'Se reciben varias muestras tisulares irregulares, blandas, desflecadas y pardo-grisáceas de aspecto membranoso y esponjoso que miden entre 0.2 y 2.1 cm. y que en conjunto pesan 12 grs., entremezcladas con material hemático, íntegramente incluidas.'
    elif macros2 == 'RESTOS OVULARES 3':
        valueToSend = 'Se reciben varias muestras tisulares irregulares, blandas, desflecadas y pardo-grisáceas de aspecto membranoso y esponjoso que miden entre 0.5 y 3.2 cm. y que en conjunto pesan 57 grs., entremezcladas con material hemático, se incluyen muestras representativas.'

    elif macros2 == 'PROSTATA BILOBULADA; PIEZA OPERATORIA':
        valueToSend = 'Se recibe una muestra tisular irregular bilobulada proveniente de próstata que mide 7 cm de longitud x 5 cm. de diámetro transverso x 4.5 cm. de diámetro antero-posterior, pesa 60 gr., su superficie es blanco-parduzca y nodular. Al corte de consistencia fibroelástica presenta caras de sección heterogéneas, blanco-grisáceas con formaciones nodulares y cribosas de diferentes diámetros. Se incluyen cortes representativos.'
    elif macros2 == 'PROSTATA TRILOBULADA; PIEZA OPERATORIA':
        valueToSend = 'Se recibe una muestra tisular irregular trilobulada proveniente de próstata que mide 7 cm de longitud x 5 cm. de diámetro transverso x 4.5 cm. de diámetro antero-posterior, pesa 60 gr., su superficie es blanco-parduzca y nodular. Al corte de consistencia fibroelástica presenta caras de sección heterogéneas, blanco-grisáceas con formaciones nodulares y cribosas de diferentes diámetros. Se incluyen cortes representativos.'
    elif macros2 == 'MUESTRAS DE PROSTATA':
        valueToSend = 'Se reciben cinco muestras tisulares irregulares provenientes de próstata que miden entre  7.5 x 5.5 x 3.3 cm y 2.8 x 1.6 x 1 cm. que en conjunto pesan 122 gr., presentan una superficie blanco-parduzca y nodular. Al corte de consistencia fibroelástica presentan caras de sección heterogéneas, blanco-grisáceas con formaciones nodulares y cribosas de diferentes diámetros. Se incluyen cortes representativos.'
    elif macros2 == 'RTU DE PROSTATA':
        valueToSend = 'Son  varios fragmentos tisulares irregulares, elongados, blanco-grisáceos, de consistencia fibroelástica y superficies nodulares  que miden entre 0.4 y 0.3  cm. de longitud x 0.3 y 0.6 cm de ancho x 0.2 y 0.4 cm de espesor y que en conjunto pesan 38 gr. Se incluyen muestras representativas. '
    elif macros2 == 'MAPEO DE PROSTATA':
        valueToSend = 'Se reciben doce frascos:\n1.- Dos frascos identificados como “Ápex izquierdo”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.6 y 0.8 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n2.- Dos frascos identificados como “Media izquierda”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.7 y 0.8 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n3.- Dos frascos identificados como “Base izquierda”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.9 y 1 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 4.- Dos frascos identificados como “Ápex derecho”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.8 y 1 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 5.- Dos frascos identificados como “Media derecha”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.7 y 0.9 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 6.- Dos frascos identificados como “Base derecha”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.6 y 0.7 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.'
    elif macros2 == 'MAPEO DE PROSTATA 2':
        valueToSend = 'Se reciben doce frascos:\n 1.- Dos frascos identificados como “Ápex izquierdo”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.5 y 0.7 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 2.- Dos frascos identificados como “Media izquierda”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.6 y 0.8 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 3.- Dos frascos identificados como “Base izquierda”: Contienen cada uno a   uno y dos    fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 0.8 y 1 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 4.- Dos frascos identificados como “Ápex derecho”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.6 y 0.9 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 5.- Dos frascos identificados como “Media derecha”: Contienen cada uno a   un    fragmento tisular cilindroideo, blando y blanco-grisáceo que miden entre 0.9 y 1.1  cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 6.- Dos frascos identificados como “Base derecha”: Contienen cada uno a   uno y dos    fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 0.5 y 1 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.'
    elif macros2 == 'MAPEO PROSTATICO CON SEIS FRASCOS':
        valueToSend = 'Se reciben seis frascos:\n 1.- Un frasco identificados como “Ápex izquierdo”: Contiene tres fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 0.8  y 1.5 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 2.- Un frasco identificados como “Media izquierda”: Contiene dos fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 0.9  y 1.2 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 3.- Un frasco identificados como “Base izquierda”: Contiene dos fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 1  y 1.5 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 4.- Un frasco identificados como “Ápex derecho”: Contiene dos fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 1.1  y 1.7 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 5.- Un frasco identificados como “Media derecha”: Contiene dos fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 1.3  y 1.7 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.\n 6.- Un frasco identificados como “Base derecha”: Contiene tres fragmentos tisulares cilindroideos, blandos y blanco-grisáceos que miden entre 0.5  y 1.3 cm. de longitud x 0.1 cm. de diámetro mayor, íntegramente incluidos.'

    elif macros2 == 'UTERO SIN ANEXOS':
        valueToSend = 'Útero sin anexos que mide 7.5 cm. de longitud x 4 cm. de diámetro transverso x 3.5 cm. de diámetro antero-posterior, pesa 70 gr., el cuello uterino mide 2.5 x 2.7 cm. de diámetros x 2.5 cm. de longitud, su superficie es lisa y blanco-grisácea con orificio cervical externo transversal y permeable. Al corte el canal endocervical es permeable, el endometrio mide 0.1 cm. de espesor, el miometrio mide 1.8 cm. El cuello uterino al corte presenta caras de sección heterogéneas y blanco-grisáceas. Se incluyen cortes representativos.'
    elif macros2 == 'UTERO SIN ANEXOS MAS MIOMAS':
        valueToSend = 'Útero sin anexos que mide 00.0 cm. de longitud x 00.0 cm. de diámetro transverso x 00.0 cm. de diámetro antero-posterior, pesa 00.0 gr., el cuello uterino mide 00.0 x 00.0 cm. de diámetros x 00.0 cm. de longitud, su superficie es lisa y blanco-grisácea con orificio cervical externo transversal y permeable. Al corte el canal endocervical es permeable, el endometrio mide 00.0 cm. de espesor, el miometrio mide 00.0 cm. con presencia de 00 formaciones nodulares de localización intramural que miden entre 00.0 y 00.0 cm. de diámetros mayores que al corte presenta caras de sección heterogéneas con haces de aspecto arremolinado. El cuello uterino al corte presenta caras de sección heterogéneas y blanco-grisáceas. Se incluyen  cortes representativos.'
    elif macros2 == 'UTERO CON  ANEXOS':
        valueToSend = 'Útero con anexos que mide 00.0 cm. de longitud x 00.0 cm. de diámetro transverso x 00.0 cm. de diámetro antero-posterior, pesa 00.0 gr., el cuello uterino mide 00.0 x 00.0 cm. de diámetros mayores x 00.0 cm. de longitud, su superficie es lisa y blanco-grisácea con orificio cervical externo transversal y permeable. Al corte el canal endocervical es permeable, el endometrio mide 00.0 cm. de espesor, el miometrio mide 00.0 cm. El cuello uterino al corte presenta caras de sección heterogéneas y blanco-grisáceas. El anexo derecho con ovario que mide 00.0 x 00.0 x 00.0 cm de diámetros mayores, su superficie es blanco-grisácea, al cortes sus caras de sección son heterogéneas y blanco-grisáceas con formaciones irregulares blanquecinas y amarillentas asimismo se observa una formación quística que mide 00.0 cm. de diámetro mayor con contenido seroso en su luz. La trompa uterina derecha mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y parduzca con presencia de 00 formaciones quísticas que miden entre 00.0 y 00.0 cm. de diámetros mayores, al corte su pared mide 0.0 cm de espesor y su luz es puntiforme permeable. Se incluyen cortes representativos. El anexo izquierdo con ovario que mide 00.0 x 00.0 x 00.0 cm de diámetros mayores, su superficie es blanco-grisácea, al cortes sus caras de sección son heterogéneas y blanco-grisáceas con formaciones irregulares blanquecinas y amarillentas asimismo se observa una formación quística que mide 00.0 cm. de diámetro mayor con contenido seroso en su luz. La trompa uterina izquierda mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y parduzca con presencia de 00 formaciones quísticas que miden entre 00.0 y 00.0 cm. de diámetros mayores, al corte su pared mide 0.0 cm de espesor y su luz es puntiforme permeable. Se incluyen cortes representativos.'
    elif macros2 == 'UTERO CON  ANEXOS MAS MIOMAS':
        valueToSend = 'Útero con anexos que mide 00.0 cm. de longitud x 00.0 cm. de diámetro transverso x 00.0 cm. de diámetro antero-posterior, pesa 00.0 gr., el cuello uterino mide 00.0 x 00.0 cm. de diámetros x 00.0 cm. de longitud, su superficie es lisa y blanco-grisácea con orificio cervical externo transversal y permeable. Al corte el canal endocervical es permeable, el endometrio mide 00.0 cm. de espesor, el miometrio mide 00.0 cm. con presencia de 00 formaciones nodulares de localización intramural que miden entre 00.0 y 00.0 cm. de diámetros mayores que al corte presenta caras de sección heterogéneas con haces de aspecto arremolinado. El cuello uterino al corte presenta caras de sección heterogéneas y blanco-grisáceas. Se toman incluyen cortes representativos. El anexo derecho con ovario que mide 00.0 x 00.0 x 00.0 cm de diámetros mayores, su superficie es blanco-grisácea, al cortes sus caras de sección son heterogéneas y blanco-grisáceas con formaciones irregulares blanquecinas y amarillentas asimismo se observa una formación quística que mide 00.0 cm. de diámetro mayor con contenido seroso en su luz. La trompa uterina derecha mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y parduzca con presencia de 00 formaciones quísticas que miden entre 00.0 y 00.0 cm. de diámetros mayores, al corte su pared mide 0.0 cm de espesor y su luz es puntiforme permeable. Se incluyen cortes representativos. El anexo izquierdo con ovario que mide 00.0 x 00.0 x 00.0 cm de diámetros mayores, su superficie es blanco-grisácea, al cortes sus caras de sección son heterogéneas y blanco-grisáceas con formaciones irregulares blanquecinas y amarillentas asimismo se observa una formación quística que mide 00.0 cm. de diámetro mayor con contenido seroso en su luz. La trompa uterina izquierda mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y parduzca con presencia de 00 formaciones quísticas que miden entre 00.0 y 00.0 cm. de diámetros mayores, al corte su pared mide 0.0 cm de espesor y su luz es puntiforme permeable. Se incluyen cortes representativos. '
    
    elif macros2=='COLECISTITIS CRONICA': 
        valueToSend = 'Vesícula biliar abierta que mide 8 cm. de longitud x 4 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 0.1 cm. de espesor y su mucosa es granular fina pardo-verdosa. Se incluyen cortes representativos.'
    elif macros2 =='COLECISTITIS CRONICA LITIASICA':
        valueToSend = 'Vesícula biliar abierta que mide 8 cm. de longitud x 4 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 0.2 cm. de espesor, su mucosa es granular fina pardo-verdosa y su lumen contiene varios cálculos pardo-amarillentos de aspecto facetado que miden entre 0 y 0 cm. Se incluyen cortes representativos.'
    elif macros2=='COLECISTITIS CRONICA LITIASICA MAS GANGLIO':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa y su lumen contiene varios cálculos pardo-amarillentos de aspecto facetado que miden entre 00.0 y 00.0 cm. El ganglio cístico está presente y mide 00 x 00 cm. Se incluyen cortes  representativos.'
    elif macros2=='COLECISTITIS CRONICA COLESTEROLOSICA':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00 cm. de espesor, su mucosa es granular fina pardo-blanquecina con estrías amarillentas. Se incluyen cortes representativos.'
    elif macros2=='COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00 cm. de espesor, su mucosa es granular fina pardo-blanquecina con estrías amarillentas y su lumen contiene varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. Se incluyen cortes representativos.'
    elif macros2=='COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA MAS GANGLIO CISTICO':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00 cm. de espesor, su mucosa es granular fina pardo-blanquecina con estrías amarillentas y su lumen contiene varios cálculos pardo-amarillentos de aspecto morular que miden entre 00 y 00 cm. de diámetros mayores. El ganglio cístico está presente y mide 0 x 0 cm. Se incluyen cortes representativos.'
    elif macros2=='COLECISTITIS CRONICA ESCLEROSANTE':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared está aumentada de consistencia, mide 00 cm. de espesor, su mucosa es trabecular pardo-blanquecina con placas blanco-amarillentas induradas. Se incluyen cortes  representativos.'
    elif macros2=='COLECISTITIS CRONICA ESCLEROSANTE LITIASICA':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared está aumentada de consistencia, mide 00 cm. de espesor, su mucosa es trabecular pardo-blanquecina con placas blanco-amarillentas induradas y su lumen contiene varios cálculos blanco-amarillentos de aspecto facetado que miden entre 0 y 0 cm. de diámetros mayores. Se incluyen  cortes representativos.'
    elif macros2=='COLECISTITIS AGUDA':
        valueToSend = 'Vesícula biliar abierta que mide 6.3 cm. de longitud x 3.5 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared es elástica, mide 0.3 cm. de espesor y su mucosa es granular pardo-grisácea oscura. Se incluyen cortes representativos.'
    elif macros2=='COLECISTITIS AGUDA LITIASICA':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00 cm. de espesor, su mucosa es granular pardo-grisácea oscura y su lumen  contiene varios cálculos pardo-grisáceos de aspecto facetado que miden entre 0 y 0 cm. Se incluyen cortes representativos.'
    elif macros2=='COLECISTITIS AGUDA LITIASICA MAS GANGLIO CISTICO':
        valueToSend = 'Vesícula biliar abierta que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00 cm. de espesor, su mucosa es granular pardo-grisácea oscura y su lumen  contiene varios cálculos pardo-grisáceos de aspecto facetado que miden entre 0 y 0 cm. El ganglio cístico está presente y mide 0 x 0 cm. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS CRONICA':
        valueToSend = 'Vesícula biliar cerrada que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00 cm. de espesor, su mucosa es granular fina pardo-verdosa y su lumen contiene líquido biliar. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS CRONICA LITIASICA':
        valueToSend = 'Vesícula biliar cerrada que mide 00 cm. de longitud x 00 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00 cm. de espesor, su mucosa es granular fina pardo-verdosa y su lumen contiene varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS CRONICA LITIASICA MAS GANGLIO':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa y su lumen contiene varios cálculos pardo-amarillentos de aspecto morular que miden entre 00 y 00 cm. El ganglio cístico está presente y mide 00.0 x 00.0 cm. Se incluyen  cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS CRONICA COLESTEROLOSICA':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa con estrías amarillentas. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa con estrías amarillentas y su lumen contiene varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA MAS GANGLIO CISTICO':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa con estrías amarillentas y su lumen contiene varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. de diámetros mayores. El ganglio cístico está presente y mide 00.0 x 00.0 cm. de diámetros mayores. Se incluyen   cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS AGUDA':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00.0 cm. de espesor y su mucosa es granular pardo-grisácea oscura. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS AGUDA LITIASICA':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00.0 cm. de espesor, su mucosa es granular pardo-grisácea oscura y su lumen  contiene varios cálculos pardo-grisáceos de aspecto faceloide que miden entre 00.0 y 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB CERRADA COLECISTITIS AGUDA LITIASICA MAS GANGLIO CISTICO':
        valueToSend = 'Vesícula biliar cerrada que mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00.0 cm. de espesor, su mucosa es granular pardo-grisácea oscura y su lumen  contiene varios cálculos pardo-grisáceos de aspecto faceloide que miden entre 00.0 y 00.0 cm. de diámetros mayores. El ganglio cístico está presente y mide 00.0 x 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS CRONICA':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor y su mucosa es granular fina pardo-verdosa. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS CRONICA LITIASICA':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa y adjunto vienen varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS CRONICA LITIASICA MAS GANGLIO':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa y adjunto vienen varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. de diámetros mayores. El ganglio cístico está presente y mide 00.0 x 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS CRONICA COLESTEROLOSICA':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa con estrías amarillentas. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS CRONICA COLESTEROLOSICA LITIASICA':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y blanco-grisácea. Al corte su pared es elástica, mide 00.0 cm. de espesor, su mucosa es granular fina pardo-verdosa con estrías amarillentas y adjunto vienen  varios cálculos pardo-amarillentos de aspecto morular que miden entre 00.0 y 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS AGUDA':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00.0 cm. de espesor y su mucosa es granular pardo-grisácea oscura. Se incluyen cortes representativos.'
    elif macros2=='VB FRAGMENTADA COLECISTITIS AGUDA LITIASICA':
        valueToSend = 'Vesícula biliar fragmentada en 0 segmentos que en conjunto mide 00.0 cm. de longitud x 00.0 cm. de diámetro mayor, su serosa es lisa y pardo-grisácea oscura con áreas de hemorragia. Al corte su pared está aumentada de consistencia, mide 00.0 cm. de espesor, su mucosa es granular pardo-grisácea oscura y adjunto vienen varios cálculos pardo-grisáceos de aspecto faceloide que miden entre 00.0 y 00.0 cm. de diámetros mayores. Se incluyen cortes representativos.'

    context = {'sent':valueToSend}
    return render(request, 'macros3.html', context)

def View_Informe_Anat(request):

    if not request.user.is_staff:
        return redirect('admin_login')
    inf = InformeAnatomico.objects.all()
    i = {'inf': inf}

    return render(request, 'view_informe_anat.html',i)

def Ver_Informe_Anat(request,pid):

    if not request.user.is_staff:
        return redirect('admin_login')
    paciente = InformeAnatomico.objects.get(id=pid)
    i = {'paciente': paciente}

    return render(request, 'ver_informe_anat.html',i)

def Report_Anat(request,pid):
    error = ""
    # Create a file-like buffer to receive PDF data.
    if request.method == "POST":
        
        firma = request.POST['firma']
        logo = request.POST['logo']
        
        # Create a file-like buffer to receive PDF data.
        locale.setlocale(locale.LC_ALL, 'es_BO.utf8')
        paciente = InformeAnatomico.objects.get(id=pid)
        buffer = io.BytesIO()
        

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer,pagesize=letter)
        width, height = letter
        
        c=4.5

        my_Style=ParagraphStyle('Mine', alignment=TA_CENTER, fontName='Helvetica', fontSize = 10)
        p1=Paragraph('''<b><u>INFORME DE ANATOMIA PATOLOGICA</u></b>''',my_Style)
        p1.wrapOn(p,width,10)
        p1.drawOn(p,0,height-c*cm)

        my_Style2=ParagraphStyle('Mine2', alignment=TA_LEFT, fontName='Helvetica', fontSize = 10)
        styles = getSampleStyleSheet()
        style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)

        m=2
        
        tbl_data = [[Paragraph("Nombre:"+' '+paciente.NombresInformeAnatomico+'  '+paciente.ApellidosInformeAnatomico, my_Style2), 
        Paragraph("Edad:"+' '+ str(paciente.EdadInformeAnatomico)+ "años", my_Style2)], 
        [Paragraph("Medico:"+' '+ paciente.MedicoInformeAnatomico, my_Style2), 
        Paragraph("Hospital/Clinica:"+' '+paciente.HospitalInformeAnatomico, my_Style2)], 
        [Paragraph("Muestra:"+' '+ paciente.MuestraInformeAnatomico, my_Style2), 
        Paragraph("Diagnostico:"+' '+paciente.DiagnosticoInformeAnatomico, my_Style2)],
        [Paragraph("Fecha de Recepcion:"+' '+ str(paciente.RecepcionInformeAnatomico.strftime("%d-%m-%Y")), my_Style2),]]
        tbl = Table(tbl_data)
        tbl.wrapOn(p,width-4*cm,3*cm)
        tbl.drawOn(p,2*cm,(22-m)*cm)
    

        p.line(0+2*cm,(21.5-m)*cm,width-2*cm,(21.5-m)*cm)

        if logo == 'SI':
            p2=Paragraph('''<img src="hospital/static/images/logo.jpg" width="100" height="80"/>''', style=styles["Normal"])
            p2.wrapOn(p,width,10)
            p2.drawOn(p,2.5*cm,height-c*cm)

        my_Style_suelto=ParagraphStyle('Mine', alignment=TA_JUSTIFY, fontName='Helvetica',splitLongWords=True, fontSize = 10)
        
        conclusion_chaine_old = paciente.ConclusionInformeAnatomico
        new_string = '<br />'
        nchar_conclusion = len(conclusion_chaine_old)
        nlines_conclusion = (conclusion_chaine_old.count('\n'))
        resultant_string = conclusion_chaine_old.replace('\n', new_string)
        micros_chaine_old  = paciente.EstudioMicroscopicoInformeAnatomico
        nchar_micros = len(micros_chaine_old)
        nlines_micros = nchar_micros // 100 + (micros_chaine_old.count('\n'))
        resultant_micros = micros_chaine_old.replace('\n',new_string)
        macros_chaine_old  = paciente.EstudioMacroscopicoInformeAnatomico
        nchar_macros = len(macros_chaine_old)
        nlines_macros = nchar_macros // 100 + (macros_chaine_old.count('\n')) 
        resultant_macros = macros_chaine_old.replace('\n',new_string)
        
        # p.showPage()
        
        if (nlines_macros+nlines_micros>12 or nlines_conclusion>10):
            
            pfirstpage=Paragraph('''<b>ESTUDIO MACROSCOPICO:</b> <br /> <br />'''
                         + resultant_macros 
                         + '''<br /> <br /> <b>ESTUDIO MICROSCOPICO:</b> <br /> <br />'''
                         + resultant_micros ,my_Style_suelto)
            pfirstpage.wrapOn(p,width-4*cm,2*cm)
            pfirstpage.drawOn(p,2*cm,(19.5-(((nlines_macros+nlines_micros)//2)+4))*cm)
            
            p.line(0+2*cm,5.5*cm,width-2*cm,5.5*cm)
            p6=Paragraph(paciente.LugarInformeAnatomico+', '+str(paciente.FechaPieInformeAnatomico.strftime("%B %d, %Y")),my_Style_suelto)
            p6.wrapOn(p,width-4*cm,2*cm)
            p6.drawOn(p,2*cm,5*cm)
    
            my_Style_suelto_der=ParagraphStyle('Mine', alignment=TA_RIGHT, fontName='Helvetica', fontSize = 10)

            if firma=='NO':

                p7=Paragraph(paciente.DoctorInformeAnatomico.Name
                             + '''<br />'''
                             + paciente.DoctorInformeAnatomico.special
                             + '''<br />'''
                             + paciente.DoctorInformeAnatomico.matricula,my_Style_suelto_der )
                p7.wrapOn(p,width-4*cm,2*cm)
                p7.drawOn(p,2*cm,2*cm)

            p10=Paragraph(paciente.CodigoInformeAnatomico,my_Style_suelto_der )
            p10.wrapOn(p,width-4*cm,2*cm)
            p10.drawOn(p,2*cm,height-c*cm)

            if firma == 'SI':
                p11=Paragraph('''<img src="hospital/static/images/FIRMA_BN.jpeg" width="100" height="80"/>''', style_right)
                p11.wrapOn(p,width-4*cm,2*cm)
                p11.drawOn(p,2*cm,2*cm)

            p.line(0+2*cm,1.5*cm,width-2*cm,1.5*cm)
            p12=Paragraph('Direccion: Z/villa dolores, calle 6. No 50. Piso 2 Oficina 8',my_Style_suelto)
            p12.wrapOn(p,width-4*cm,2*cm)
            p12.drawOn(p,2*cm,1*cm)
            
            p.showPage()
            
            p1=Paragraph('''<b><u>INFORME DE ANATOMIA PATOLOGICA</u></b>''',my_Style)
            p1.wrapOn(p,width,10)
            p1.drawOn(p,0,height-c*cm)
        
            tbl_data = [[Paragraph("Nombre:"+' '+paciente.NombresInformeAnatomico+'  '+paciente.ApellidosInformeAnatomico, my_Style2), 
            Paragraph("Edad:"+' '+ str(paciente.EdadInformeAnatomico)+ "años", my_Style2)], 
            [Paragraph("Medico:"+' '+ paciente.MedicoInformeAnatomico, my_Style2), 
             Paragraph("Hospital/Clinica:"+' '+paciente.HospitalInformeAnatomico, my_Style2)], 
            [Paragraph("Muestra:"+' '+ paciente.MuestraInformeAnatomico, my_Style2), 
            Paragraph("Diagnostico:"+' '+paciente.DiagnosticoInformeAnatomico, my_Style2)],
            [Paragraph("Fecha de Recepcion:"+' '+ str(paciente.RecepcionInformeAnatomico.strftime("%d-%m-%Y")), my_Style2),]]
            tbl = Table(tbl_data)
            tbl.wrapOn(p,width-4*cm,3*cm)
            tbl.drawOn(p,2*cm,(22-m)*cm)
    

            p.line(0+2*cm,(21.5-m)*cm,width-2*cm,(21.5-m)*cm)

            if logo == 'SI':
                p2=Paragraph('''<img src="hospital/static/images/logo.jpg" width="100" height="80"/>''', style=styles["Normal"])
                p2.wrapOn(p,width,10)
                p2.drawOn(p,2.5*cm,height-c*cm)
            
            psecondpage=Paragraph( '''<b>ESPECIMEN:</b> '''
                         + paciente.EspecimenInformeAnatomico 
                         + '''<br /> <br /> <b>CONCLUSION:</b> <br /> <br />'''
                         + resultant_string
                        #  + '''<br /> <br /> <b>numerolineas micmac:</b> <br /> <br />'''
                        #  + str(nlines_macros+nlines_micros)
                        #  + '''<br /> <br /> <b>numerolineas concl:</b> <br /> <br />'''
                        #  + str(nlines_conclusion) 
                        ,my_Style_suelto)
            psecondpage.wrapOn(p,width-4*cm,2*cm)
            psecondpage.drawOn(p,2*cm,(19.5-(((nlines_conclusion)//2)+4))*cm)
            
            p.line(0+2*cm,5.5*cm,width-2*cm,5.5*cm)
            p6=Paragraph(paciente.LugarInformeAnatomico+', '+str(paciente.FechaPieInformeAnatomico.strftime("%B %d, %Y")),my_Style_suelto)
            p6.wrapOn(p,width-4*cm,2*cm)
            p6.drawOn(p,2*cm,5*cm)
    
            my_Style_suelto_der=ParagraphStyle('Mine', alignment=TA_RIGHT, fontName='Helvetica', fontSize = 10)

            if firma=='NO':

                p7=Paragraph(paciente.DoctorInformeAnatomico.Name
                             + '''<br />'''
                             + paciente.DoctorInformeAnatomico.special
                             + '''<br />'''
                             + paciente.DoctorInformeAnatomico.matricula,my_Style_suelto_der )
                p7.wrapOn(p,width-4*cm,2*cm)
                p7.drawOn(p,2*cm,2*cm)

            p10=Paragraph(paciente.CodigoInformeAnatomico,my_Style_suelto_der )
            p10.wrapOn(p,width-4*cm,2*cm)
            p10.drawOn(p,2*cm,height-c*cm)

            if firma == 'SI':
                p11=Paragraph('''<img src="hospital/static/images/FIRMA_BN.jpeg" width="100" height="80"/>''', style_right)
                p11.wrapOn(p,width-4*cm,2*cm)
                p11.drawOn(p,2*cm,2*cm)

            p.line(0+2*cm,1.5*cm,width-2*cm,1.5*cm)
            p12=Paragraph('Direccion: Z/villa dolores, calle 6. No 50. Piso 2 Oficina 8',my_Style_suelto)
            p12.wrapOn(p,width-4*cm,2*cm)
            p12.drawOn(p,2*cm,1*cm)
            
        else:
            
            p4=Paragraph('''<b>ESTUDIO MACROSCOPICO:</b> <br /> <br />'''
                         + resultant_macros 
                         + '''<br /> <br /> <b>ESTUDIO MICROSCOPICO:</b> <br /> <br />'''
                         + resultant_micros 
                         + '''<br /> <br /> <br /> <br /> <b>ESPECIMEN:</b> '''
                         + paciente.EspecimenInformeAnatomico 
                         + '''<br /> <br /> <b>CONCLUSION:</b> <br /> <br />'''
                         + resultant_string ,my_Style_suelto)
            p4.wrapOn(p,width-4*cm,2*cm)
            p4.drawOn(p,2*cm,(19.5-(((nlines_macros+nlines_micros+nlines_conclusion)//2)+8))*cm)

            p.line(0+2*cm,5.5*cm,width-2*cm,5.5*cm)
            p6=Paragraph(paciente.LugarInformeAnatomico+', '+str(paciente.FechaPieInformeAnatomico.strftime("%B %d, %Y")),my_Style_suelto)
            p6.wrapOn(p,width-4*cm,2*cm)
            p6.drawOn(p,2*cm,5*cm)
    
            my_Style_suelto_der=ParagraphStyle('Mine', alignment=TA_RIGHT, fontName='Helvetica', fontSize = 10)

            if firma=='NO':

                p7=Paragraph(paciente.DoctorInformeAnatomico.Name
                             + '''<br />'''
                             + paciente.DoctorInformeAnatomico.special
                             + '''<br />'''
                             + paciente.DoctorInformeAnatomico.matricula,my_Style_suelto_der )
                p7.wrapOn(p,width-4*cm,2*cm)
                p7.drawOn(p,2*cm,2*cm)

            p10=Paragraph(paciente.CodigoInformeAnatomico,my_Style_suelto_der )
            p10.wrapOn(p,width-4*cm,2*cm)
            p10.drawOn(p,2*cm,height-c*cm)

            if firma == 'SI':
                p11=Paragraph('''<img src="hospital/static/images/FIRMA_BN.jpeg" width="100" height="80"/>''', style_right)
                p11.wrapOn(p,width-4*cm,2*cm)
                p11.drawOn(p,2*cm,2*cm)

            p.line(0+2*cm,1.5*cm,width-2*cm,1.5*cm)
            p12=Paragraph('Direccion: Z/villa dolores, calle 6. No 50. Piso 2 Oficina 8',my_Style_suelto)
            p12.wrapOn(p,width-4*cm,2*cm)
            p12.drawOn(p,2*cm,1*cm)
        
        

        textob=p.beginText()
        textob.setTextOrigin(cm,cm)
        textob.setFont("Helvetica",14)
    
        
        p.setTitle("INFORME_ANATOMICO"+'_'
                   +paciente.ApellidosInformeAnatomico+'_'
                   +str(paciente.FechaPieInformeAnatomico.strftime("%B_%d_%Y")))
    
        title = "INFORME_ANATOMICO"+'_'+paciente.ApellidosInformeAnatomico+'_'+str(paciente.FechaPieInformeAnatomico.strftime("%B_%d_%Y"))+".pdf"
        
        p.drawText(textob)
        p.showPage()
        p.save()

        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=title)
    
    d = {'error':error}
    return render(request, 'report_signature_logo.html',d)

def Upd_Datos_Paciente_Anat(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeAnatomico.objects.get(id=pid)

    fecha_recepcion = paciente.RecepcionInformeAnatomico.strftime("%Y-%m-%d")
    
    if request.method == "POST":
        
        cod=request.POST['Codigo']
        
        nom = request.POST['Nombres']
        ape = request.POST['Apellidos']
        ed = request.POST['Edad']
        med = request.POST['Medico']
        hosp = request.POST['Hospital']
        mues = request.POST['Muestra']
        diag = request.POST['Diagnostico']
        
        rec = request.POST['Recepcion']
        
        try:
            paciente.CodigoInformeAnatomico = cod
            paciente.NombresInformeAnatomico = nom
            paciente.ApellidosInformeAnatomico = ape
            paciente.EdadInformeAnatomico = ed
            paciente.MedicoInformeAnatomico = med
            paciente.HospitalInformeAnatomico = hosp
            paciente.MuestraInformeAnatomico = mues
            paciente.DiagnosticoInformeAnatomico = diag
            paciente.RecepcionInformeAnatomico = rec
            paciente.save()
            
            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'fecha_recepcion':fecha_recepcion}
    return render(request, 'upd_datos_paciente_anat.html', d)

def Upd_Tabla_Central_Paciente_Anat(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeAnatomico.objects.get(id=pid)

    if request.method == "POST":
        
        estmic = request.POST['EstudioMicro']
        estmac = request.POST['EstudioMacro']
        try:
            paciente.EstudioMacroscopicoInformeAnatomico=estmac
            paciente.EstudioMicroscopicoInformeAnatomico=estmic
        
            paciente.save()

            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente}
    return render(request,'upd_tabla_central_paciente_anat.html', d)

def Upd_Conclusion_Paciente_Anat(request,pid):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    paciente = InformeAnatomico.objects.get(id=pid)
    vector_lugar = ["La Paz", "El Alto"]
    

    fecha_informe = paciente.FechaPieInformeAnatomico.strftime("%Y-%m-%d")
    
    
    if request.method == "POST":
        
        conclu = request.POST['Conclusion']
        espec = request.POST['Especimen']
        fech = request.POST['FechaPie']
        lug = request.POST['Lugar']
        
        try:
            paciente.EspecimenInformeAnatomico= espec 
            paciente.ConclusionInformeAnatomico= conclu
            paciente.FechaPieInformeAnatomico = fech
            paciente.LugarInformeAnatomico = lug
            paciente.save()

            error = "no"
        except:
            error ="yes"

    
    d = {'error':error,'paciente':paciente,'lugar':vector_lugar,'fechainf':fecha_informe}
    return render(request,'upd_conclusion_paciente_anat.html', d)

def Delete_Informe_Anat(request,pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    informeAnat = InformeAnatomico.objects.get(id=pid)
    
    informeAnat.delete()

    return redirect('view_informe_anat')
