# from django.contrib import admin
from django.urls import path
from .views import About,Home,Contact,Index,Login,Logout_admin,View_Doctor,Delete_Doctor,Add_Doctor, View_Patient,Delete_Patient,Add_Patient,View_Appointment, Add_Appointment, Delete_Appointment, Add_Informe,View_Informe, Delete_Informe, Ver_Informe, Report
from .views import Add_Informe_Cit,Upd_Datos_Paciente,Upd_Muestra_Paciente,Upd_Tabla_Central_Paciente, Upd_Conclusion_Paciente

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('admin_login/', Login, name='admin_login'),
    path('logout/', Logout_admin, name='logout_admin'),
    path('index/', Index, name='dashboard'),
    path('view_doctor/', View_Doctor, name='view_doctor'),
    path('add_doctor/', Add_Doctor, name='add_doctor'),
    path('view_patient/', View_Patient, name='view_patient'),
    path('view_appointment/', View_Appointment, name='view_appointment'),
    path('add_patient/', Add_Patient, name='add_patient'),
    path('add_appointment/', Add_Appointment, name='add_appointment'),
    path('delete_doctor(?p<int:pid>)/', Delete_Doctor, name='delete_doctor'),
    path('delete_patient(?p<int:pid>)/', Delete_Patient, name='delete_patient'),
    path('delete_appointment(?p<int:pid>)/', Delete_Appointment, name='delete_appointment'),

    path('add_informe/',Add_Informe,name='add_informe'),
    path('view_informe/',View_Informe,name='view_informe'),
    path('delete_informe(?p<int:pid>)/', Delete_Informe, name='delete_informe'),
    path('ver_informe(?p<int:pid>)/',Ver_Informe,name='ver_informe'),

    path('report(?p<int:pid>)/',Report,name='report'),
    path('add_informe_cit/',Add_Informe_Cit,name='add_informe_cit'),

    path('upd_datos_paciente(?p<int:pid>)/',Upd_Datos_Paciente, name='upd_datos_paciente'),
    path('upd_muestra_paciente(?p<int:pid>)/',Upd_Muestra_Paciente, name='upd_muestra_paciente'),
    path('upd_tabla_central_paciente(?p<int:pid>)/',Upd_Tabla_Central_Paciente, name='upd_tabla_central_paciente'),
    path('upd_conclusion_paciente(?p<int:pid>)/',Upd_Conclusion_Paciente, name='upd_conclusion_paciente'),


]
