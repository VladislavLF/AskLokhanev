from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from app import views as views_app
from app.views import custom_404, custom_403
from users import views as views_users


handler404 = custom_404
handler403 = custom_403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_app.index, name="index"),
    path('hot/', views_app.hot, name="hot"),
    path('tag/<int:tag_id>/', views_app.tag, name="tag"),
    path('question/<int:question_id>/', views_app.question, name="question"),
    path('login/', views_users.LoginUser.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page=None), name='logout'),
    path('signup/', views_users.RegisterUser.as_view(), name="signup"),
    path('ask/', views_app.ask, name="ask"),
    path('settings/', views_users.ProfileUser.as_view(), name="settings"),
    path('rate/', views_app.rate_object, name='rate_object'),
    path('answer/correct/', views_app.toggle_correct_answer, name='toggle_correct_answer'),
    path('search/', views_app.search_page, name='search_page'),
    path('search_questions/', views_app.search_questions, name='search_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
