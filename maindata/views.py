from .models import Cost, Paid, Medicin, File, Session, Patient,Reserve,SessionPrice
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
import json
def createvisitforreserve(request,pk):
    reserve_id = pk
    # url = reverse('maindata:createvisitforreserve', args=[reserve_id] )

    reserve_data = Reserve.objects.get(id = reserve_id) 
    try:
        patient = Patient.objects.filter(national_id = reserve_data.national_id)[0]
    except:
        patient=Patient.objects.create(national_id = reserve_data.national_id , phone_number = reserve_data.phone_number,name=reserve_data.name)
        patient.save()

    new_session = Session.objects.create(patient = patient , visit_type = reserve_data.visit_type)
    new_session.save()
    new_session_price = 0
    session_price_cost = None
    current_session_price = SessionPrice.objects.last()
    if new_session.visit_type == 'N':
        try:
            new_session_price = current_session_price.new_session_price
        except:
            pass
        session_price_cost = Cost.objects.create(session = new_session,cost = new_session_price,reason = 'كشف جديد')
    else:
        try:
            new_session_price = current_session_price.return_session_price
        except:
            pass
        session_price_cost = Cost.objects.create(session = new_session,cost = new_session_price,reason = ' اعادة كشف')
    
    session_price_cost.save()
    reserve_data.status = True
    reserve_data.save()
    return redirect('admin:maindata_session_change',new_session.id)

def addpaid(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        session_id = data.get('session_id')
        paid = data.get('paid')
        
        session = Session.objects.get(id=session_id)
        # sessionreport = session.sessionreport()
        Paid.objects.create(session=session, paid=paid)
    
    #     return redirect(request.path)
    return HttpResponse({'paid':paid})

def getactivevisiturl(self):
    active_session = Session.objects.last()
    active_url = reverse('admin:maindata_session_change', args=[active_session.id] )
    return JsonResponse({'active_url':active_url})