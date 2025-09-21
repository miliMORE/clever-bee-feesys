from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def post_login_redirect(request):
    # Staff go to admin; others to home
    return redirect('/admin/') if request.user.is_staff else redirect('/')
