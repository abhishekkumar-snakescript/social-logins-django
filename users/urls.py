from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("set-password/", views.set_password, name="set_password"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("post-login-redirect/", views.post_login_redirect, name="post_login_redirect"),
    # path('privacy/data-deletion/', views.DataDeletionView.as_view(), name='data_deletion')
]