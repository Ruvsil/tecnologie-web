from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
def home(request):
    ctx ={}
    return render(request, template_name='home.html', context=ctx)

def recommend(user):
    pass

def base(request):
    user = get_object_or_404(User, pk=request.user.pk)
    recommended_list = recommend(user)
    ctx = {'recommended_list': recommended_list}
    return render(request, template_name='base.html', context=ctx)