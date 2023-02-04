from django.shortcuts import render,redirect

from django.views.generic import CreateView,FormView,ListView,DetailView,View,TemplateView
from django.urls import reverse_lazy
from customer.forms import RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from api.models import Products,Carts,Orders
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]

class SignUpView(CreateView):
    template_name="signup.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request,"account created successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"account creation failed ")
        return super().form_invalid(form)


class SignInView(FormView):
    template_name="signin.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("user-home")
            else:
                messages.error(request,"Invalid credentials")
                return render(request,"signin.html",{"form":form})

@method_decorator(decs,name="dispatch")
class HomeView(ListView):
    template_name="cust-index.html"
    context_object_name="products"
    model=Products

@method_decorator(decs,name="dispatch")   
class ProductDetailView(DetailView):
    template_name="cust-productdetail.html"
    context_object_name="product"
    pk_url_kwarg="id"
    model=Products

decs
def addto_cart(request,*args,**kwargs):
    id=kwargs.get("id")
    product=Products.objects.get(id=id)
    user=request.user
    Carts.objects.create(user=user,product=product)
    messages.success(request,"item has been added to cart")
    return redirect("user-home")

@method_decorator(decs,name="dispatch")
class CartProductView(ListView):
    template_name="cart-list.html"
    context_object_name="items"
    model=Carts

    def get(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user,status="in-cart")
        total=Carts.objects.filter(user=request.user,status="in-cart").aggregate(tot=Sum("product__price"))
        return render(request,"cart-list.html",{"carts":qs,"total":total})

    # def get_queryset(self):
    #     return Carts.objects.filter(user=self.request.user)

decs
def SignOutView(request,*args,**kwargs):
    logout(request)
    return redirect('login')

@method_decorator(decs,name="dispatch")
class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Carts.objects.get(id=id).delete()
        return redirect('cart-lists')

@method_decorator(decs,name="dispatch")
class OrderView(TemplateView):
    template_name="checkout.html"
    def get(self,request,*args,**kwargs):
        pid=kwargs.get('pid')
        qs=Products.objects.get(id=pid)
        return render(request,"checkout.html",{"product":qs})
    
    def post(self,request,*args,**kwargs):
        pid=kwargs.get('pid')
        cid=kwargs.get('cid')
        cart=Carts.objects.get(id=cid)
        product=Products.objects.get(id=pid)
        user=request.user
        address=request.POST.get("address")
        mobile=request.POST.get("mobile")
        Orders.objects.create(product=product,user=user,address=address,phone=mobile)
        cart.status="order-placed"
        cart.save()
        messages.success(request,"your order has been placed")
        return redirect("user-home")

@method_decorator(decs,name="dispatch")    
class MyOrdersView(ListView):
    model=Orders
    template_name="order-list.html"
    context_object_name="orders"

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)

decs
def CancelOrderView(request,*args,**kwargs):
    id=kwargs.get('id')
    Orders.objects.filter(id=id).update(status="cancelled")
    messages.success(request,"order is cancelled and removed")
    return redirect('user-home')