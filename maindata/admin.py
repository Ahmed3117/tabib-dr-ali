from django.contrib import admin
from .models import Cost, Paid, Medicin, File, Session, Patient,Reserve,SessionPrice
from django.urls import reverse
from django.utils.html import format_html
from django.middleware.csrf import get_token
from django.template.loader import render_to_string

class CostInline(admin.TabularInline):
    model = Cost
    extra = 0

class PaidInline(admin.TabularInline):
    model = Paid
    extra = 0

class MedicinInline(admin.TabularInline):
    model = Medicin
    extra = 0

class FileInline(admin.TabularInline):
    model = File
    extra = 0

class SessionInline(admin.TabularInline):
    model = Session
    extra = 0

class SessionPriceAdmin(admin.ModelAdmin):
    list_display = ('new_session_price', 'return_session_price')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date_added', 'visit_type', 'diagnosis','sessionmidicin')
    list_filter = ('patient__name', 'date_added', 'visit_type')
    search_fields = ('patient__name', 'diagnosis')
    inlines = [MedicinInline, FileInline,CostInline, PaidInline]
    change_list_template = 'admin/maindata/Session/change_list.html'
    # def showvisits(self, obj):
    #     patient_id = obj.id
    #     url = reverse('admin:maindata_session_changelist')
    #     url += f'?patient_id={patient_id}'
    #     return format_html('<a class="button rounded " href="{}"> الزيارات</a>', url)
    # showvisits.short_description = ' الزيارات '
    def sessionmidicin(self, obj):
        session_id = obj.id
        session_medicins = obj.medicin_set.all()
        modal_html = render_to_string('admin/maindata/session/session_midicin.html', {
            'session_id' : session_id,
            'session_medicins' : session_medicins,
        })
        return format_html(modal_html)

    # def sessioninfo(self, obj):
    #     session_id = obj.id
    #     session = Session.objects.get(id = session_id)
    #     costs = Cost.objects.filter(session = session)
    #     session_costs = 0
    #     for cost in costs:
    #         if cost.cost :
    #             session_costs += cost.cost
    #     paids = Paid.objects.filter(session = session)
    #     session_paids = 0
    #     for paid in paids:
    #         if paid.paid :
    #             session_paids += paid.paid
    #     modal_html = render_to_string('admin/maindata/session/session_info.html', {
    #         'session_id' : session_id,
    #         'session_costs' : session_costs,
    #         'session_paids' : session_paids,
    #     })
    #     return format_html(modal_html)
    sessionmidicin.short_description = ' روشتة '
    # sessioninfo.short_description = ' معلومات '

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_id', 'phone_number', 'address','date_added','showvisits','report', 'notes')
    search_fields = ('name', 'national_id', 'phone_number', 'address', 'notes')
    def showvisits(self, obj):
        patient_id = obj.id
        url = reverse('admin:maindata_session_changelist')
        url += f'?patient_id={patient_id}'
        return format_html('<a class="button rounded " href="{}"> الزيارات</a>', url)
    showvisits.short_description = ' الزيارات '
    
    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context=extra_context)
        
    def report(self, obj):
        patient_id = obj.id
        total_session_costs = obj.patientreport()[0]
        total_session_paids = obj.patientreport()[1]
        charge = obj.patientreport()[2]
        sessions = obj.patientreport()[3]
        url = reverse('maindata:addpaid', args=[patient_id])
        csrf_token = get_token(self.request)
        
        modal_html = render_to_string('admin/maindata/patient/report.html', {
            'patient_id' : patient_id,
            'total_session_costs' : total_session_costs,
            'total_session_paids' : total_session_paids,
            'charge' : charge,
            'sessions' : sessions,
            'url': url,
            'csrf_token': csrf_token,
        })
        return format_html(modal_html)
    report.short_description = ' تقرير بالحساب '

class ReserveAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_id', 'phone_number', 'address','date_added','specific_time','visit_type','status','startvisit')
    list_filter = ('name', 'national_id')
    search_fields = ('name', 'national_id', 'phone_number', 'address')
    ordering = ('status','date_added','specific_time')
    # list_editable = ('visit_type',)
    def startvisit(self, obj):
        reserve_id = obj.id
        url = reverse('maindata:createvisitforreserve', args=[reserve_id] )

        active_reserve_objs = Reserve.objects.filter(status = True)
        active_reserve_obj = list(active_reserve_objs)[-1]

        active_session = Session.objects.last()
        active_url = reverse('admin:maindata_session_change', args=[active_session.id] )
        # url += f'?pk={reserve_id}'
        if obj == active_reserve_obj:
            
            return format_html('<a class="button rounded "href="{0}">  نشطة</a>', active_url)
        elif obj.status == False:
            return format_html('<a class="button rounded " href="{0}"> ابدأ</a>', url)
        else :
            
            return None
    startvisit.short_description = ' حالة الزيارة '

admin.site.register(Cost)
admin.site.register(Paid)
admin.site.register(Medicin)
admin.site.register(File)
admin.site.register(Session, SessionAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(SessionPrice, SessionPriceAdmin)

