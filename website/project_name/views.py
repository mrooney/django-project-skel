from coffin.shortcuts import render_to_response
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect
from django.template import RequestContext
import cjson

def r2r(template, request, data=None):
    data = data or {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def superuser_required(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

def json_response(func):
    def decorated(*args, **kwargs):
        return HttpResponse(cjson.encode(func(*args, **kwargs)), mimetype="application/json")
    return decorated

def home(request):
    return r2r("index.jinja", request)

def login(request):
    def failure(error_msg):
        return r2r("login.jinja", request, locals())

    if request.method == "GET":
        return r2r("login.jinja", request, locals())
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login_user(request, user)
                # Redirect to a success page.
                return redirect("home")
            else:
                # Return a 'disabled account' error message
                return failure("This account has been disabled.")
        else:
            # Return an 'invalid login' error message.
            return failure("Invalid email address or password.")

def logout(request):
    logout_user(request)
    return redirect("home")

def signup(request):
    if request.method == "GET":
        return r2r("signup.jinja", request, locals())
    else:
        email = request.POST['email']
        password = request.POST['password']
        if not email_re.match(email):
            error_msg = "Please enter a valid email address."
            return r2r("signup.jinja", request, locals())
        if len(password) < 6:
            error_msg = "Please enter a password of at least 6 characters."
            return r2r("signup.jinja", request, locals())
        if User.objects.filter(username=email).count():
            error_msg = "An account with this email address already exists."
            return r2r("signup.jinja", request, locals())

        user = User.objects.create_user(email, email, password=password)
        user.save()
        user = authenticate(username=email, password=password)
        login_user(request, user)
        return redirect("home")

@login_required
def account(request):
    profile = request.user.get_profile()

    if request.method == "POST":
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']

        if pw1 or pw2:
            if pw1 == pw2:
                request.user.set_password(pw1)
                request.user.save()
            else:
                error = "Passwords do not match."
        message = "Settings successfully updated."

    return r2r("settings.jinja", request, locals())

