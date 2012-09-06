"""
Dummy Authentication
"""

from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect


# No social stuff
STATUS_UPDATES = False


class LoginForm(forms.Form):
  username = forms.CharField(max_length=50)
  admin_p = forms.BooleanField(required=False, initial=False, label='Admin?')


def login_view(request):
  # imports are here because putting them in the header prevents
  # initialization of the database
  from helios_auth.view_utils import render_template
  from helios_auth.views import after
  from helios_auth.models import User

  if request.method == "GET":
    form = LoginForm()
  else:
    form = LoginForm(request.POST)
    request.session['auth_system_name'] = 'dummy'

    if request.POST.has_key('return_url'):
      request.session['auth_return_url'] = request.POST.get('return_url')

    if form.is_valid():
      name = form.cleaned_data['username'].strip()
      admin_p = form.cleaned_data['admin_p']
      user_obj = User.update_or_create(user_type='dummy', user_id=name, name=name, info={})
      if user_obj.admin_p != admin_p:
        user_obj.admin_p = admin_p
        user_obj.save()
      request.session['dummy_user'] = name
      return HttpResponseRedirect(reverse(after))

  return render_template(request, 'dummy/login', {'form': form})


def get_auth_url(request, redirect_url = None):
  return reverse(login_view)


def get_user_info_after_auth(request):
  name = request.session['dummy_user']
  del request.session['dummy_user']
  return {'type': 'dummy', 'user_id': name, 'name': name, 'info': {}, 'token': None}
