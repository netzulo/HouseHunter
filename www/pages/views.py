from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Page

# Create your views here.


def index(request):
    context = {
        "pages": Page.objects.order_by('id')
    }
    try:
        return render(request, "pages/index.html", context)
    except Exception:
        raise Http404("ERROR: Can't render pages view")
