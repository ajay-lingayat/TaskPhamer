from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Designer.urls')),
    path('accounts/', include('accounts.urls')),
]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'TaskPhamer'
admin.site.index_title = 'TaskPhamer administration'

handler404 = 'Designer.views.Error404'
handler403 = 'Designer.views.Error403'
handler500 = 'Designer.views.Error500'