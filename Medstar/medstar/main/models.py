from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=50)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, blank=True, null=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    phone_numder = models.CharField(max_length=30)
    password = models.CharField(max_length=70)
    is_director = models.BooleanField()
    on_vacation = models.BooleanField()

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} {self.patronymic}'

class Department(models.Model):
    title = models.CharField(max_length=70)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id} / {self.title} / {self.hospital}"

class Hospital(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Patient(models.Model):
    BloodTypes = [
        ('I положительная', '1+'),
        ('I отрицательная', '1-'),
        ('II положительная', '2+'),
        ('II отрицательная', '2-'),
        ('III положительная', '3+'),
        ('III отрицательная', '3-'),
        ('IV положительная', '4+'),
        ('IV отрицательная', '4-'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    birth_date = models.DateField()
    blood_type = models.CharField(choices=BloodTypes, max_length=17)
    additiona_information = models.TextField(blank=True)
    diseases = models.ManyToManyField('Disease', blank=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    phone_numder = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Reference(models.Model):
    text = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    today_date = models.DateTimeField()
    next_date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    next_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='next_doctor')
    lenght = models.PositiveIntegerField(default=20)
    all_day = models.BooleanField()

    def __str__(self):
        return f'{self.id} \ {self.patient} \ {self.doctor} \ {self.text} \ {self.all_day}'