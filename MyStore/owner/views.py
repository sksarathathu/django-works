from django.shortcuts import render
from django.contrib.auth.models import User



# Create your views here.
from django.views.generic import View
from owner.forms import LoginForm,RegistrationForm,ProductForm


class HomeView(View):
    def get(self,request,*args,**kwargs):

        return render(request,"home.html",)


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
            return render(request,"login.html")
        else:
            return render(request,"register.html",{"form":form})


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

class ProductView(View):
    def get(self,request,*args,**kwargs):
        form=ProductForm()
        return render(request,"products.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"home.html")
        else:
            return render(request,"products.html",{"form":form})

