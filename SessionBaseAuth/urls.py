from django.urls import path, include, re_path

from rest_framework import routers
from accounts.views import AccountsViewSet

router = routers.SimpleRouter()
router.register(r"accounts", AccountsViewSet, basename = "accounts"),

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    #path('api/', include(router.urls)),
    #path('api/instances/', AccountsViewSet.as_view(), name = "register"),

]

urlpatterns += router.urls


#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]