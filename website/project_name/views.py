from coffin.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect
from django.template import RequestContext
import cjson

def r2r(template, request, data=None):
    data = data or {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def json_response(func):
    def decorated(*args, **kwargs):
        return HttpResponse(cjson.encode(func(*args, **kwargs)), mimetype="application/json")
    return decorated

