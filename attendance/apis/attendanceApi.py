import secrets, random, base64
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone
from ..helpers.responseHelper import api_response 

from ..models.sessionModel import Session
from ..models.attendanceModel import Attendance
import qrcode
import json

from django.views.decorators.csrf import csrf_exempt


from django.utils import timezone

# Generate QR session
def get_qr(request):
    token = secrets.token_urlsafe(8)
    numeric_code = f"{random.randint(10, 99)}"
    s = Session.objects.create(token=token, numeric_code=numeric_code)

    # TODO: Replace with actual frontend URL
    mobile_url = f'http://127.0.0.1:8000/attendance/get_code/{token}/'

    # Generate QR image (base64)
    qr = qrcode.make(mobile_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Generate numeric code choices
    numeric_choices = {numeric_code}
    print(numeric_choices)
    
    while len(numeric_choices) < 5:
        numeric_choices.add(f"{secrets.randbelow(90) + 10}")
    numeric_choices = list(numeric_choices)
    secrets.SystemRandom().shuffle(numeric_choices)


   
    return api_response(
        True,
        "QR generated successfully",
        {
            'token': token,
            'mobile_url': mobile_url,
            'numeric_code_choices': numeric_choices,
            'qr_base64': qr_base64,
        }
    )


# Check session status
def status(request, token):
    try:
        s = Session.objects.get(token=token)
        return api_response(True, "Session found", {"verified": s.verified})
    except Session.DoesNotExist:
        return api_response(False, "Session not found", status=404)


# Get numeric code
def get_code(request, token):
    try:
        s = Session.objects.get(token=token)
        return api_response(
            True,
            "Code retrieved",
            {"code": s.numeric_code}
        )
    except Session.DoesNotExist:
        return api_response(False, "Session not found", status=404)
# Confirm signin / signout
@csrf_exempt
@require_POST
def confirm(request, token):
    s = get_object_or_404(Session, token=token)
    
    try:
        data = json.loads(request.body)
        code = data.get('code')
    except (json.JSONDecodeError, TypeError):
        return api_response(False, "Invalid request", status=400)

    if code == s.numeric_code:
        user, _ = User.objects.get_or_create(username='demo_user')

        s.verified = True
        s.verified_by = user
        s.save()

        open_attendance = Attendance.objects.filter(
            user=user, signout_at__isnull=True
        ).last()

        if open_attendance:
            open_attendance.signout_at = timezone.now()
            open_attendance.save()
            action = "signout"
        else:
            Attendance.objects.create(
                user=user,
                device='mobile',
                scan_session=s,
                signin_at=timezone.now()
            )
            action = "signin"

        return api_response(True, "Action completed", {"action": action})
    else:
        return api_response(False, "Invalid code", status=400)
# Attendance records
def records_list(request):
    records = list(
        Attendance.objects
        .select_related('user')
        .order_by('-timestamp')[:50]
        .values('id', 'timestamp', 'user__username')
    )
    return api_response(True, "Records fetched", {"records": records})
