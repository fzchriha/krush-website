from django.shortcuts import render

#Logic for landing page only an html file
def landing_home(request):
    return render(request, 'landing/landing.html')
