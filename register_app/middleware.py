from django.http import HttpResponseRedirect


class NoAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user

        if not user.is_authenticated:
            return None

        # Define your custom logic here. For example:
        if view_func.__name__ == 'admin_dashboard' and not user.is_staff:
            return HttpResponseRedirect('/no_access/')

        return None
