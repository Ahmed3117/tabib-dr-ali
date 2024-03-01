from django.db import models

class SessionPrice(models.Model):
    new_session_price = models.IntegerField(verbose_name = " سعر الكشف الجديد",default = 1 ,null=True,blank=True)
    return_session_price = models.IntegerField(verbose_name = " سعر اعادة الكشف",default = 1 ,null=True,blank=True)
    class Meta:
        verbose_name_plural = ' اسعار الزيارات'
        verbose_name='   حسبة'
    def __str__(self) :
        try:
            return str(self.new_session_price)
        except:
            return 'غير معروف'

class Patient(models.Model):
    name = models.CharField(verbose_name = " الاسم",max_length=200,null=True,blank=True)
    national_id = models.CharField(verbose_name = " الرقم القومى",max_length=14 ,null=True,blank=True)
    phone_number = models.CharField(verbose_name = " رقم التليفون ",max_length=20,null=True,blank=True )
    address = models.CharField(verbose_name = "  العنوان ",max_length=100,null=True,blank=True )
    notes = models.CharField(verbose_name = "  ملاحظات ",max_length=200,null=True,blank=True )
    date_added = models.DateTimeField(verbose_name = " تاريخ الاضافة",auto_now_add=True,null=True,blank=True) 
    def patientreport(self):
        patient_id = self.id
        sessions = Session.objects.filter(patient = self)
        
        total_session_costs = 0
        total_session_paids = 0
        for session in sessions :
            costs = Cost.objects.filter(session = session)
            session_costs = 0
            for cost in costs:
                if cost.cost :
                    session_costs += cost.cost
            paids = Paid.objects.filter(session = session)
            session_paids = 0
            for paid in paids:
                if paid.paid :
                    session_paids += paid.paid
            total_session_costs += session_costs
            total_session_paids += session_paids
        

        charge = total_session_costs - total_session_paids
        return total_session_costs , total_session_paids , charge,sessions
    class Meta:
        verbose_name_plural = '  حسابات المرضى'
        verbose_name='   حساب'
    def __str__(self) :
        try:
            return self.name
        except:
            return 'غير معروف'

class Session(models.Model): 
    visittype = (
        ('N' , 'جديد'),
        ('R' , 'اعادة')
    )
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "الحالة ") 
    date_added = models.DateTimeField(verbose_name = " تاريخ الزيارة",auto_now_add=True,null=True,blank=True) 
    visit_type = models.CharField(verbose_name = " نوع الزيارة",choices=visittype,editable=True,default='N',max_length=10,null=True,blank=True)
    diagnosis = models.TextField(verbose_name = "  التشخيص",max_length=1000,null=True,blank=True)
    # session_file = models.FileField(upload_to='session_files/',null=True,blank=True,verbose_name = "  ملف")
    
    class Meta:
        verbose_name_plural = '  الزيارات'
        verbose_name='   زيارة'
    def __str__(self) :
        try:
            return self.patient.name
        except:
            return 'غير معروف'

class Medicin(models.Model):
    takentime = (
        ('a' , 'بعد الاكل'),
        ('b' , 'قبل الاكل'),
        ('c' , 'قبل الاكل وبعده'),
        ('d' , 'قبل النوم'),
        ('e' , ' صباحا'),
        ('f' , ' مساءا'),
        ('g' , ' صباحا ومساءا'),
        ('h' , '  كل 6 ساعات'),
        ('i' , '  كل 12 ساعة'),
        ('j' , '  كل 24 ساعة'),
        ('k' , '  كل 48 ساعة')
    )
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " الزيارة") 
    name = models.CharField(verbose_name = "  اسم العلاج",max_length=200,null=True,blank=True)
    times = models.IntegerField(verbose_name = "عدد المرات",default = 1 ,null=True,blank=True)
    taken_time = models.CharField(verbose_name = "  التوقيت",choices=takentime,max_length=10,null=True,blank=True)
    # status = models.BooleanField(verbose_name='الحالة' , default=True,null=True,blank=True)
    day_times = models.IntegerField(verbose_name = "عدد ايام المواظبة",default = 1 ,null=True,blank=True)
    class Meta:
        verbose_name_plural = '  العلاج'
        verbose_name='   علاج'
    def __str__(self) :
        try:
            return self.session.patient.name
        except:
            return 'غير معروف'

class Cost(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " الزيارة") 
    cost = models.IntegerField(verbose_name = " تكلفة",default = 1 ,null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الاستحقاق",auto_now_add=True,null=True,blank=True) 
    reason = models.CharField(verbose_name = "  سبب التكلفة",default='كشف',max_length=200,null=True,blank=True)
    class Meta:
        verbose_name_plural = ' مصاريف'
        verbose_name=' تكلفة'
    def __str__(self) :
        try:
            return self.session.patient.name
        except:
            return 'غير معروف'
            
class Paid(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " الزيارة") 
    paid = models.IntegerField(verbose_name = " المدفوع",default = 1 ,null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الدفع",auto_now_add=True,null=True,blank=True) 
    class Meta:
        verbose_name_plural = ' المدفوعات'
        verbose_name=' دفعة'
    def __str__(self) :
        try:
            return self.session.patient.name
        except:
            return 'غير معروف'

# class PatentPay(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " الحالة") 
#     paid = models.IntegerField(verbose_name = " المدفوع",default = 1 ,null=True,blank=True)
#     date_added = models.DateTimeField(verbose_name = " تاريخ الدفع",auto_now_add=True,null=True,blank=True) 
#     class Meta:
#         verbose_name_plural = ' المدفوع لاحقا'
#         verbose_name=' دفعة'
#     def __str__(self) :
#         try:
#             return self.patient.name
#         except:
#             return 'غير معروف'

class File(models.Model):
    title = models.CharField(max_length=255,verbose_name = "  وصف")
    session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " الزيارة") 
    file = models.FileField(upload_to='session_files/',null=True,blank=True,verbose_name = "  ملف")
    datet_added = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True,verbose_name = "  الحالة")
    class Meta:
        verbose_name_plural = ' (تحاليل , اشاعات , ...) الملفات'
        verbose_name='   ملف'
    def __str__(self) :
        try:
            return self.title
        except:
            return 'غير معروف'

# class AllMedicin(models.Model):
    # takentime = (
    #     ('a' , 'بعد الاكل'),
    #     ('b' , 'قبل الاكل'),
    #     ('c' , 'قبل الاكل وبعده'),
    #     ('d' , 'قبل النوم'),
    #     ('e' , ' صباحا'),
    #     ('f' , ' مساءا'),
    #     ('g' , ' صباحا ومساءا'),
    #     ('h' , '  كل 6 ساعات'),
    #     ('i' , '  كل 12 ساعة'),
    #     ('j' , '  كل 24 ساعة'),
    #     ('k' , '  كل 48 ساعة')
    # )
    # session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " الزيارة") 
    # name = models.CharField(verbose_name = "  اسم العلاج",max_length=200,null=True,blank=True)
    # times = models.IntegerField(verbose_name = "عدد المرات",default = 1 ,null=True,blank=True)
    # taken_time = models.CharField(verbose_name = "  التوقيت",choices=takentime,default='a',max_length=10,null=True,blank=True)
    # status = models.BooleanField(verbose_name='الحالة' , default=True,null=True,blank=True)
    # class Meta:
    #     verbose_name_plural = '  العلاج'
    #     verbose_name='   علاج'
    # def __str__(self) :
    #     try:
    #         return self.session.patient.name
    #     except:
    #         return 'غير معروف'

class Reserve(models.Model):
    visittype = (
        ('N' , 'جديد'),
        ('R' , 'اعادة')
    )
    name = models.CharField(verbose_name = " الاسم",max_length=200,null=True,blank=True)
    national_id = models.CharField(verbose_name = " الرقم القومى",max_length=14 ,null=True,blank=True)
    phone_number = models.CharField(verbose_name = " رقم التليفون ",max_length=20,null=True,blank=True )
    address = models.CharField(verbose_name = "  العنوان ",max_length=100,null=True,blank=True )
    status = models.BooleanField(verbose_name = "  حالة الانتهاء ",default=False )
    date_added = models.DateTimeField(verbose_name = " تاريخ الاضافة",auto_now_add=True,null=True,blank=True) 
    specific_time = models.TimeField(verbose_name = "  الوقت",default = "00-00-00",null=True,blank=True) 
    visit_type = models.CharField(verbose_name = " نوع الزيارة",choices=visittype,editable=True,default='N',max_length=10,null=True,blank=True)

    class Meta:
        verbose_name_plural = '   الحجوزات'
        verbose_name='   حجز'
        ordering = ('status',)
        
    def __str__(self) :
        try:
            return self.name
        except:
            return 'غير معروف'
