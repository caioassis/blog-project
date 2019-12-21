from functools import wraps
import requests
from django.conf import settings
from django.contrib import messages


def recaptcha_required(f):
    @wraps(f)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response', None)
            if not recaptcha_response:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.', extra_tags='danger')
            else:
                url = settings.GOOGLE_RECAPTCHA_URL
                data = {
                    'secret': settings.GOOGLE_RECAPTCHA_KEY,
                    'response': recaptcha_response
                }
                r = requests.post(url, data)
                res = r.json()
                request.recaptcha_is_valid = res['success']
                if not request.recaptcha_is_valid:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.', extra_tags='danger')
        return f(request, *args, **kwargs)
    return _wrapped_view
