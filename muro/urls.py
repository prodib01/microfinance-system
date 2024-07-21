from django.contrib import admin
from django.urls import path, include
from .views import loans, financialstatements, download_loans_pdf, reports, test, search_loan, sec_page
from users.views import logout_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    path('', include('homeApp.urls')),
    path('loans/', loans, name='loans'),
    path('loan/', include('loan.urls')),
    path('financialstatements/', financialstatements, name='financialstatements'),
    path('reports/', reports, name='reports'),
    path('reports/download/pdf/', download_loans_pdf, name='download-loans-pdf'),
    # path('clientview/', clientview, name='clientview'),
    path('clients/', include('clientApp.urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('api.v1.urls')),
    path('test/', test, name='test'),
    path('search-loan/', search_loan, name='search-loan'),
    path('sec-page/', sec_page, name='sec-page'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'MURO Administration'
admin.site.site_title = 'MURO Administration'
admin.site.index_title = 'MURO Administration'

