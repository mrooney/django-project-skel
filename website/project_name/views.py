from coffin.shortcuts import render_to_response
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout as logout_user, login as login_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect
from django.template import RequestContext

import cjson
import uuid
import re

from {{project_name}} import models

email_re = re.compile(
     r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
     # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
     r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
     r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)'  # domain
     r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE # literal form, ipv4 address (SMTP 4.1.3)
)
      
def r2r(template, request, data=None):
    data = data or {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def is_valid_email(email):
    return True if email_re.match(email) else False

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
    usermodel = get_user_model()
    if request.method == "GET":
        return r2r("signup.jinja", request, locals())
    else:
        email = request.POST['email']
        password = request.POST['password']
        if not is_valid_email(email):
            error_msg = "Please enter a valid email address."
            return r2r("signup.jinja", request, locals())
        if len(password) < 6:
            error_msg = "Please enter a password of at least 6 characters."
            return r2r("signup.jinja", request, locals())
        if usermodel.objects.filter(username=email).count():
            error_msg = "An account with this email address already exists."
            return r2r("signup.jinja", request, locals())

        user = usermodel.objects.create_user(email, email, password=password)
        user.save()
        user = authenticate(username=email, password=password)
        login_user(request, user)

        # Send email confirmation.
        email_confirm_url = reverse('email_confirm', args=[str(uuid.uuid4())])
        msg = "Thanks for signing up for {{project_name}}!\n\nPlease confirm your email address by clicking the following link: {0}{1}. You won't be able to receive further emails from us until confirming your address.\n\nIf you didn't sign up, take no action, and this is the last email you'll receive from us.\n\nThanks,\n{0}".format(settings.WEBSITE_URL, email_confirm_url)
        user.email_user("Welcome to {{project_name}}", msg, ignore_confirmed=True)

        return redirect("home")

@login_required
def email_confirm(request, token):
    request.user.email_confirmed = True
    request.user.save()
    return r2r("email_confirmed.jinja", request, locals())

@login_required
def account(request):
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

def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None):

    from {{project_name}}.forms import PasswordResetForm as password_reset_form
    from django.contrib.auth.tokens import default_token_generator as token_generator

    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            form.save(**opts)
            return redirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = { 'form': form }
    if extra_context is not None:
        context.update(extra_context)
    return r2r(template_name, request, context)

def password_reset_done(request):
    message = "We've e-mailed you your username and instructions for resetting your password to the e-mail address you submitted. You should be receiving it shortly."
    messages.success(request, message)
    return redirect('home')

