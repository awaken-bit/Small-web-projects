from medstar.settings import MY_TIME_ZONE
from main.models import Department, Disease, Doctor, Patient
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import Http404
from authorization.views import query_debugger
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
import datetime


def index(request):
    user = request.user
    if user.is_authenticated:
        data = {
            'page': 'main',
            'references': user.doctor.next_doctor.order_by('next_date').filter(next_date__gt=datetime.datetime.now() 
                                                                               + datetime.timedelta(hours=MY_TIME_ZONE) - datetime.timedelta(minutes=30))
        }
    else:
        data = {
            'page': 'main',
        }
    return render(request, 'main/main.html', data)

@query_debugger
def all_references(request):
    user = request.user
    if user.is_authenticated and user.doctor.is_director:
        references = user.doctor.hospital.reference_set.select_related('hospital', 'doctor', 'next_doctor', 'patient')
        speks = request.GET

        # Фильтры
        if speks.get('today_date_from'):
            references = references.filter(today_date__gt=speks.get('today_date_from'))

        if speks.get('today_date_to'):
            references = references.filter(today_date__lt=speks.get('today_date_to'))

        if speks.get('next_date_from'):
            references = references.filter(next_date__gt=speks.get('next_date_from'))

        if speks.get('next_date_to'):
            references = references.filter(next_date__lt=speks.get('next_date_to'))


        if speks.get('sorting'):
            sorting = speks.get('sorting')
            if sorting == 'next_date_from_old':
                references = references.order_by('next_date')
            elif sorting == 'next_date_from_new':
                references = references.order_by('-next_date')
            elif sorting == 'today_date_from_old':
                references = references.order_by('today_date')
            elif sorting == 'today_date_from_new':
                references = references.order_by('-today_date')
        
        if speks.get('patient'):
            try:
                references = references.filter(patient_id=int(speks.get('patient')))
            except:
                pass

        if speks.get('doctor'):
            try:
                references = references.filter(doctor_id=int(speks.get('doctor')))
            except:
                pass

        if speks.get('next_doctor'):
            try:
                references = references.filter(next_doctor_id=int(speks.get('next_doctor')))
            except:
                pass

        references = Paginator(references, 20)
        page_number = speks.get('page')
        print(speks)

        references = references.get_page(page_number)

        data = {
            'references': references,
            'range_references': list(references.paginator.get_elided_page_range(references.number, on_ends = 1)),
            'page': 'references',
            'parametrs': speks.dict()
        }
        return render(request, 'main/references.html', data)
    else:
        raise Http404

def patients_view(request):
    if request.user.is_authenticated:
        patients = request.user.doctor.hospital.patient_set.order_by('-id').all()
        patients_and_date = []
        for i in patients:
            patients_and_date.append([i, i.birth_date.strftime("%d-%m-%Y")])
        data = {
            'page': 'patients',
            'diseases': Disease.objects.all(),
            'patients': patients_and_date,
            'lenght': len(patients_and_date)
        }
        return render(request, 'main/patients_view.html', data)
    else:
        raise Http404

@query_debugger
def edit_patient(request):
    if request.method == 'POST' and request.user.is_authenticated:
        speks = request.POST
        doctor = request.user.doctor
        
        print(speks)
        
        try:
            speks['id']
            speks['first_name']
            speks['last_name']
            speks['patronymic']
            speks['birth_date']
            speks['blood_type']
            speks['phone']

            patient = doctor.hospital.patient_set.get(id=int(speks.get('id')))
        except:
            raise Http404
        
        patient.first_name = speks.get('first_name')
        patient.last_name = speks.get('last_name')
        patient.patronymic = speks.get('patronymic')
        patient.birth_date = speks.get('birth_date')
        patient.blood_type = speks.get('blood_type')
        patient.phone_numder = speks.get('phone')
        patient.additiona_information = speks.get('additiona_information')

        patient.diseases.clear()
        for i in speks.getlist('datalist'):
            try:
                disease = Disease.objects.get(name=i)
            except:
                disease = Disease(
                    name = i
                )
                disease.save()
            patient.diseases.add(disease)

        patient.save()
        
        return redirect('patients_view')
    else:
        raise Http404

@query_debugger
def add_patient(request):
    if request.method == 'POST' and request.user.is_authenticated:
        speks = request.POST
        print(speks)
        try:
            speks['first_name']
            speks['last_name']
            speks['patronymic']
            speks['birth_date']
            speks['blood_type']
            speks['phone']
        except:
            raise Http404
        
        if  len(speks.get('birth_date').split('-')[0]) > 4:
            raise Http404

        patient = Patient(
            first_name = speks.get('first_name'),
            last_name = speks.get('last_name'),
            patronymic = speks.get('patronymic'),
            birth_date = speks.get('birth_date'),
            blood_type = speks.get('blood_type'),
            additiona_information =  speks.get('additiona_information'),
            hospital = request.user.doctor.hospital,
            phone_numder = speks.get('phone')
        )
        patient.save()
        diseases = []
        for i in speks.getlist('datalist'):
            try:
                disease = Disease.objects.get(name=i)
            except:
                disease = Disease(
                    name = i
                )
                disease.save()
            diseases.append(disease.id)
        patient.diseases.add(*diseases)

        return redirect('patients_view')
    else:
        raise Http404

def delete_patient(request, pk):
    if request.user.is_authenticated:
        try:
            patient = request.user.doctor.hospital.patient_set.get(id = pk)
        except:
            raise Http404('Нет пациента с таким id')
        patient.delete()
        return redirect('patients_view')
    else:
        raise Http404

# Управление больницей
def edit_hospital_title(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.doctor.is_director:
        speks = request.POST
        hospital = request.user.doctor.hospital

        try:
            speks['title']
        except:
            raise Http404('Ошибка в данных')
        if hospital.title != speks.get('title'):
            hospital.title = speks.get('title')
            hospital.save()
        return redirect('management')
    else:
        raise Http404

# Управление персоналом
def hospital_management(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            raise Http404
        else:
            doctors =  request.user.doctor.hospital.doctor_set.order_by('-user_id').all()
            data = {
                'doctors': doctors,
                'page': 'management',
                'is_director': user.doctor.is_director,
                'departments': request.user.doctor.hospital.department_set.all()
            }

            return render(request, 'main/hospital_management.html', data)
    else:
        raise Http404

@query_debugger
def create_doctor(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.doctor.is_director:
        speks = request.POST
        try:
            speks['password']
            speks['first_name']
            speks['last_name']
            speks['patronymic']
            speks['department']
            speks['position']
            speks['phone']
        except:
            raise Http404('Ошибка в данных')
        
        user = User(
            first_name = speks.get('first_name'),
            last_name = speks.get('last_name'),
            password = speks['password']
        )
        user.save()
        user.username = user.id
        user.save()

        if speks.get('department'):
            try:
                department = request.user.doctor.hospital.department_set.get(title=speks.get('department'))
            except:
                department = Department(
                    hospital = request.user.doctor.hospital, 
                    title = speks.get('department')
                )
                department.save()
        else:
            department = None
        
        doctor = Doctor(
            user = user,
            patronymic = speks.get('patronymic'),
            is_director = 'is_director' in speks,
            hospital = request.user.doctor.hospital,
            position = speks.get('position'),
            password = speks.get('password'),
            phone_numder = speks.get('phone'),
            on_vacation = 'on_vacation' in speks,
            department = department
        )
        doctor.save()
        
        
        return redirect('management')
    else:
        raise Http404

@query_debugger
def edit_doctor(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.doctor.is_director:
        speks = request.POST
        print(speks)
        try:
            doctor = request.user.doctor.hospital.doctor_set.select_related('user', 'department').get(
                user_id=int(speks.get('login')))
            speks['password']
            speks['first_name']
            speks['last_name']
            speks['patronymic']
            speks['department']
            speks['position']
            speks['phone']
        except:
            raise Http404('Ошибка в данных')

        change_password = False

        if speks.get('password') != doctor.password:
            change_password = True
            doctor.user.set_password(speks.get('password'))
            doctor.password = speks.get('password')

        doctor.user.first_name = speks.get('first_name')
        doctor.user.last_name = speks.get('last_name')
        doctor.patronymic = speks.get('patronymic')

        if speks.get('department'):
            try:
                department = request.user.doctor.hospital.department_set.get(title = speks.get('department'))
            except:
                department = Department(
                    hospital = request.user.doctor.hospital, 
                    title = speks.get('department')
                )
                department.save()
            doctor.department = department

        doctor.position = speks.get('position')
        doctor.phone_number = speks.get('phone')
        doctor.on_vacation = 'on_vacation' in speks
        doctor.is_director = 'is_director' in speks


        doctor.user.save()
        doctor.save()
        if request.user.doctor == doctor and change_password:
            authenticate_user = authenticate(username=request.user.id, password=speks.get('password'))
            if authenticate_user is not None:
                if authenticate_user.is_active:
                    login(request, authenticate_user)
                else:
                    raise Http404('Отключенная учетная запись')
            else:
                raise Http404('Неверный логин или пароль')
        
        return redirect('management')
    else:
        raise Http404

@query_debugger
def delete_doctor(request, pk):
    if request.user.is_authenticated and request.user.doctor.is_director:
        try:
            doctor = request.user.doctor.hospital.doctor_set.get(user_id = pk)
        except:
            raise Http404('Нет доктора с таким логином')
        doctor.delete()

        return redirect('management')
    else:
        raise Http404
