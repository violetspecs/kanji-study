from django.http.response import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return HttpResponseRedirect(reverse('quiz:index'))