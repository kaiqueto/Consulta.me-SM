from django.contrib import admin
from django.contrib.auth import views as auth_views  # views prontas de login/logout do Django
from django.urls import path, include               # path() cria rotas, include() delega para outro arquivo
from django.conf import settings
from django.conf.urls.static import static          # serve os uploads (/media/) em desenvolvimento

urlpatterns = [
    # Painel administrativo do Django
    path('admin/', admin.site.urls),

    # Login com a LoginView pronta do Django, usando o nosso template
    path('login/', auth_views.LoginView.as_view(template_name='intranet/login.html'), name='login'),

    # Logout (precisa ser POST — o botão "Sair" do menu envia um formulário)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Todas as outras rotas ficam no app intranet (intranet/urls.py)
    path('', include('intranet.urls')),

# static(): com DEBUG=True, serve os arquivos enviados que ficam em /media/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
