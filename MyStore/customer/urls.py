from django.urls import path
from customer import views

urlpatterns=[
    path("register",views.SignUpView.as_view(),name="register"),
    path("",views.SignInView.as_view(),name="login"),
    path("customers/home",views.HomeView.as_view(),name="user-home"),
    path("products/details/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/addtocart/<int:id>",views.addto_cart,name="addto-cart"),
    path("customers/carts-list",views.CartProductView.as_view(),name="cart-lists"),
    path("logout",views.SignOutView,name="logout"),
    path("cart-delete/<int:id>",views.CartDeleteView.as_view(),name="cart-delete"),
    path("orders/add/<int:cid>/<int:pid>",views.OrderView.as_view(),name="place-order"),
    path("orders/list",views.MyOrdersView.as_view(),name="order-list"),
    path("orders/<int:id>/remove",views.CancelOrderView,name="order-cancel")

]