from django.shortcuts import render

def home(request):
    return render(request, 'homepage/index.html')
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    return render(request, 'admin/dashboard.html')