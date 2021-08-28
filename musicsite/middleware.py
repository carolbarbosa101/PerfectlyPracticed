from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from users.models import MyUser, LoginDate


def login_exempt(view):
    view.login_exempt = True
    return view

# Middleware to require login on every view except the ones decorated with the above function
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, 'login_exempt', False):
            return

        if request.user.is_authenticated:
            return

        return login_required(view_func)(request, *view_args, **view_kwargs)


# Middleware which updates the last login & login dates of the user
class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            MyUser.objects.filter(pk=request.user.id).update(last_login=now())
            the_user = MyUser.objects.get(pk=request.user.id)

            # check last login user field
            # create login date object IF there isn't one for that day already
            last_login_date = the_user.last_login
            if(LoginDate.objects.filter(login_date=last_login_date).count() == 0):
                LoginDate.objects.create(user=the_user, login_date=last_login_date)

        response = self.get_response(request)
        return response

