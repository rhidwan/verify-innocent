from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from .models import Authentication, BlacklistIP
import csv
from datetime import datetime, timedelta

# Create your views here.
def get_ip_address(request):
    """ use requestobject to fetch client machine's IP Address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def block_or_update_blacklist(ip):
    try:
        blocked_ip = BlacklistIP.objects.get(ip_address=ip)
        if blocked_ip.hit_count < 3:
            blocked_ip.hit_count = blocked_ip.hit_count + 1
        else:
            blocked_ip.blocked = True
        blocked_ip.save()
    except:
        blocked_ip  = BlacklistIP.objects.create(ip_address=ip)
        blocked_ip.save()

def is_ip_in_blacklist(ip):
    try:
        blocked_ip = BlacklistIP.objects.get(ip_address=ip)
        return blocked_ip.blocked
    except:
        return False

def authenticate(request):
    if request.method == 'GET':
        unique_str = request.GET.get("id", None)
        # we are assigning 200 as Ok 403 as forbidden and 409 as already exists
        context = {"status": 403}
        ip = get_ip_address(request)
        if not is_ip_in_blacklist(ip):
            if not unique_str is None and not unique_str == "":
                try:
                    product = Authentication.objects.get(unique_str=unique_str)
                    if product.hit_count < 4:
                        if product.hit_count == 0:context["status"] = 200
                        elif product.authenticated:context["status"] = 409
                        print("I tr")
                        product.validated_at = datetime.now()
                        
                        product.authenticated = True
                        product.hit_count = product.hit_count + 1
                        product.ip_address = ip
                        product.save()
                        print("I executed")
                    else:
                        context["status"] = 403
                        block_or_update_blacklist(ip)
                except:
                    context["status"] = 403
                    block_or_update_blacklist(ip)
            else:
                context["status"] = 0
                block_or_update_blacklist(ip)
            return render(request, "authenticate/index.html", context=context)
        else:
            return HttpResponseForbidden()
    return HttpResponseForbidden()


def get_csv(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type='text/csv')  
        response['Content-Disposition'] = 'attachment; filename="product.csv"'  
        products = Authentication.objects.filter(inserted_at__gte = datetime.now() - timedelta(days=1))  
        writer = csv.writer(response)  
        for product in products:  
            writer.writerow([product.id, "https://verifyinnocent.com/authenticate?id=" + product.unique_str])  
        return response
    else:
        return HttpResponseForbidden()

def view_test_result(request):
    return render(request, 'authenticate/test_result.html')
