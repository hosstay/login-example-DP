from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from home import views as home_views
from accounts import views as account_views

# remember to end each path with a '/' so it works with 'resolve(/path/)' in tests
urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # auth urls
    path('register/', account_views.Register.as_view(), name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name='./accounts/login/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),

    # password reset urls
    path(
        'reset/',
        auth_views.PasswordResetView.as_view(
            template_name = './accounts/password_reset/password_reset.html',
            email_template_name = './accounts/password_reset/password_reset_email.html',
            subject_template_name = './accounts/password_reset/password_reset_subject.txt'
        ),
        name = 'password_reset'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name = './accounts/password_reset/password_reset_done.html'),
        name = 'password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name = './accounts/password_reset/password_reset_confirm.html'),
        name = 'password_reset_confirm'
    ),
    path(
        'reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name = './accounts/password_reset/password_reset_complete.html'),
        name = 'password_reset_complete'
    ),

    # password change urls
    path(
        'settings/password/', 
        auth_views.PasswordChangeView.as_view(template_name = './accounts/password_change/password_change.html'), 
        name = 'password_change'
    ),
    path(
        'settings/password/done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name = './accounts/password_change/password_change_done.html'), 
        name = 'password_change_done'
    ),

    # account urls
    path('settings/account/', account_views.EditUser.as_view(), name='my_account'),

    # BOARDS
    path('boards/', include('boards.urls')),

    # API
    path('api/', include('api.urls')),

    # HOME
    path('', include('home.urls')),
]