from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name="home"),
    path('gettags/', views.gettags, name='gettags'),
     path('fetch/', views.fetch, name="fetch"),
#    path('search_result/', views.search_result, name="search_result"),
    path('signup/', views.signup_view, name="signup"),
    path('termsandconditions/', views.terms, name="tandc"),
#    path('filelist/', views.filelist, name="filelist"),  
    path('login/', views.user_login, name="login"),
    path('upload/', views.fileupload, name = "upload"),
    path('logout/', views.user_logout, name="logout"),
    path('landing/', views.landing, name="landing"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name="about"),
    path('faq/', views.faq, name='faq'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('add/', views.profile, name='add_phone_number'),
    path('delete/<int:pk>/', views.delete_phone_number, name='delete_phone_number'),
    path('delete-email/<int:pk>/', views.delete_email, name='delete_email'),
    path('check_user_existence/', views.check_user_existence, name='check_user_existence'),
    path('send_whatsappnotify/', views.send_whatsapp_message, name="send_whatsapp_message"),

    # Password management 

    # 1 - Allow us to enter our email in order to receive a password reset link

    path('reset_password', auth_views.PasswordResetView.as_view(template_name="account/password-reset.html"), name="reset_password"),

    # 2 - Show a success message stating that an email was sent to reset our password

    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="account/password-reset-sent.html"), name="password_reset_done"),

    # 3 - Send a link to our email, so that we can reset our password + We will be prompted to enter in a new password

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password-reset-form.html"), name="password_reset_confirm"),

    # 4 - Show a success message stating that our password was changed

    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name="account/password-reset-complete.html"), name="password_reset_complete"),


]









