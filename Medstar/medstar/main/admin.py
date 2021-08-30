from django.contrib import admin
from.models import *



class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'id', 'hospital')

    def doctor(self, obj):
        return obj
    
    

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('reference', 'patient', 'doctor', 'next_doctor', 'hospital')

    def reference(self, obj):
        return obj.text if len(obj.text) < 40 else obj.text[:40]
    

class DoctorInline(admin.TabularInline):
    model = Doctor

class HospitalAdmin(admin.ModelAdmin):
    inlines = (
        DoctorInline,
    )


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Disease)
admin.site.register(Department)
admin.site.register(Hospital, HospitalAdmin)
