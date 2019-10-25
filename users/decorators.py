from django.core.exceptions import PermissionDenied


def user_access(function):
    def wrap(request, *args, **kwargs):
        if request.user.accessibility:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
