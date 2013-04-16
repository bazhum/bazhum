# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse

from db_opt.options import *

def pageChg(request):
    html = "<html><body>Added: %s</body></html>" % (modPages())
    return HttpResponse(html)