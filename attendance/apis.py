import secrets, random, base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import Session, Attendance
import qrcode

def get_qr(request):
    token = secrets.token_urlsafe(8)
    numeric_code = f"{random.randint(10, 99)}"
    s = Session.objects.create(token=token, numeric_code=numeric_code)

    # this needs to be changed with FE url
    mobile_url = 'http://localhost:5173//{token}/'
    # Generate QR image
    qr = qrcode.make(mobile_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Generate multiple numeric choices and shuffle
    numeric_choices = {numeric_code}
    while len(numeric_choices) < 5:
        numeric_choices.add(f"{secrets.randbelow(90) + 10}")
    numeric_choices = list(numeric_choices)
    secrets.SystemRandom().shuffle(numeric_choices)

    return JsonResponse( {
        'token': token,
        'mobile_url': mobile_url,
        'numeric_code_choices': numeric_choices,
        'qr_base64': qr_base64,
    })

def status(request, token):
    try:
        s = Session.objects.get(token=token)
    except Session.DoesNotExist:
        return JsonResponse({'found': False})
    return JsonResponse({'found': True, 'verified': s.verified})

def confirm(request, token):
    s = get_object_or_404(Session, token=token)
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == s.numeric_code:
            user, _ = User.objects.get_or_create(username='demo_user')
            s.verified = True
            s.verified_by = user
            s.save()
            Attendance.objects.create(user=user, device='mobile', scan_session=s)
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False, 'error': 'Invalid code'})
    return JsonResponse({'token': token})

def records_list(request):
    records = list(
        Attendance.objects
        .select_related('user')
        .order_by('-timestamp')[:50]
        .values('id', 'timestamp', 'user__username')  # choose fields you want
    )
    return JsonResponse({'records': records})
