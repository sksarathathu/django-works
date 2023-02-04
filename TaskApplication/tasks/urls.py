from django.urls import path
from tasks import views

urlpatterns=[
    path("tasks/add",views.TaskCreateView.as_view(),name="task-create"),
    path("tasks/all",views.TaskListView.as_view(),name="task-list"),
    path("tasks/<int:id>",views.TaskDetailView.as_view(),name="task-detail"),
    path("tasks/<int:id>/remove",views.TaskDeleteView.as_view(),name="task-delete"),
        path("index",views.IndexView.as_view(),name="home"),
        path("register",views.SignUpView.as_view(),name="signup"),
        path("",views.SignInView.as_view(),name="signin"),
        path("logout",views.SignOutView,name="signout")
]