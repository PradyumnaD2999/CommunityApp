from django.shortcuts import render

# Create your views here.
def groupsView(request):
    return render(request, "groups.html")