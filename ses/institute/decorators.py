from django.core.exceptions import PermissionDenied

def is_institute(function):
    def wrap(request, *args, **kwargs):
        if 'user_role' in request.session:
            if request.session['user_role'] == 'institute':
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_loggedin(function):
    def wrap(request, *args, **kwargs):
        if 'user_email' in request.session:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
