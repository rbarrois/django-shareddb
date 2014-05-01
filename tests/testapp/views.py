import json

from django import http

from . import models
# Create your views here.

def read(request):
    qs = (models.Something.objects
        .order_by('pk')
        .values('pk', 'data')
    )
    data = json.dumps(list(qs))
    return http.HttpResponse(data, content_type='application/json')
