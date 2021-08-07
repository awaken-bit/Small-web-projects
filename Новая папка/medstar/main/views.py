from main.models import Department, Disease, Doctor, Hospital
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import Http404
from authorization.views import query_debugger
from django.contrib.auth import authenticate, login




def index(request):
    data = {
        'page': 'main',
    }
    return render(request, 'main/main.html', data)

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

def edit_patient(request):
    if request.method == 'POST' and request.user.is_authenticated:
        speks = request.POST
        print(speks)
        print(speks.getlist('datalist'))
        return redirect('patients_view')
    else:
        raise Http404

# Управление больницей
def edit_hospital_title(request):
    if request.method == 'POST' and request.user.doctor.is_director:
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
    if user.is_authenticated and request.user.doctor.is_director:
        if request.method == 'POST':
            raise Http404
        else:
            doctors =  request.user.doctor.hospital.doctor_set.order_by('-user_id').all()
            data = {
                'doctors': doctors,
                'page': 'management',
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

# Other
def blood_type_format(string):
    blood_type = string.split(' ')
    answer = ''
    if blood_type[0] == 'I':
        answer += '1'
    elif blood_type[0] == 'II':
        answer += '2'
    elif blood_type[0] == 'III':
        answer += '3'
    else:
        answer += '4'
    
    if blood_type[1] == 'положительная':
        answer += '+'
    else:
        answer += '-'
    return answer