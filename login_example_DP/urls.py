"""login_example_DP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from boards import views as board_views
from accounts import views as account_views

# remember to end each path with a '/' so it works with 'resolve(/path/)' in tests
urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # auth urls
    path('signup/', account_views.signup, name = 'signup'),
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

    # board urls
    # path('', board_views.boards, name = 'boards'),
    path('', board_views.BoardListView.as_view(), name = 'boards'),
    # path('boards/<int:pk>/', board_views.board_threads, name = 'board_threads'),
    path('boards/<int:pk>/', board_views.ThreadListView.as_view(), name = 'board_threads'),
    path('boards/<int:pk>/new/', board_views.new_thread, name = 'new_thread'),

    # post urls
    path('boards/<int:pk>/threads/<int:thread_pk>/', board_views.PostListView.as_view(), name = 'view_thread'),
    path('boards/<int:pk>/threads/<int:thread_pk>/new_parent_post/', board_views.new_parent_post, name = 'new_parent_post'),
    path('boards/<int:pk>/threads/<int:thread_pk>/posts/<int:post_pk>/edit/', board_views.PostUpdateView.as_view(), name = 'edit_post'),

    # account urls
    path('settings/account/', account_views.UserUpdateView.as_view(), name='my_account'),
]