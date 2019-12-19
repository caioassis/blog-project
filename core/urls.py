from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LoginView, LogoutView, SignupView, AuthorListView, AuthorUpdateView, AuthorDeleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)