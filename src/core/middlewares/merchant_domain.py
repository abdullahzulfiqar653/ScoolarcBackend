from django.conf import settings
from django.http import HttpResponseForbidden

from api.models.merchant import Merchant


class MerchantDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]  # Extract domain without port

        merchant = Merchant.objects.filter(domain=host).first()
        if host not in settings.ALLOWED_HOSTS and not merchant:
            return HttpResponseForbidden("Merchant not found")

        request.merchant = merchant

        response = self.get_response(request)
        return response
