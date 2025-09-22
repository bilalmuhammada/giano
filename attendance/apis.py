import secrets, random, base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


from .models import Session, Attendance
import qrcode

def get_qr(request):
    token = secrets.token_urlsafe(8)
    numeric_code = f"{random.randint(10, 99)}"
    s = Session.objects.create(token=token, numeric_code=numeric_code)

    # this needs to be changed with FE url
<<<<<<< HEAD
    mobile_url = f'https://localhost:5173/mobile/{token}/'
=======
    mobile_url = 'http://localhost:5173//{token}/'
>>>>>>> frontendbranch
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

def get_code(request, token):
    try:
        s = Session.objects.get(token=token)
    except Session.DoesNotExist:
        return JsonResponse({'found': False})
    return JsonResponse({'found': True, 'code': s.numeric_code})

@require_POST
def confirm(request, token):
    s = get_object_or_404(Session, token=token)
    code = request.POST.get('code')

    if code == s.numeric_code:
        user, _ = User.objects.get_or_create(username='demo_user')

        s.verified = True
        s.verified_by = user
        s.save()

        # 🔹 Check if user already has an "open" attendance (signed in but not signed out)
        open_attendance = Attendance.objects.filter(user=user, signout_at__isnull=True).last()

        if open_attendance:
            # 👉 Update signout
            open_attendance.signout_at = timezone.now()
            open_attendance.save()
            action = "signout"
        else:
            # 👉 Create new signin
            Attendance.objects.create(
                user=user,
                device='mobile',
                scan_session=s,
                signin_at=timezone.now()
            )
            action = "signin"

        return JsonResponse({'ok': True, 'action': action})

    else:
        return JsonResponse({'ok': False, 'error': 'Invalid code'})


def records_list(request):
    records = list(
        Attendance.objects
        .select_related('user')
        .order_by('-timestamp')[:50]
        .values('id', 'timestamp', 'user__username')  # choose fields you want
    )
    return JsonResponse({'records': records})
