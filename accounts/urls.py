from django.urls import path
from .views import AccountsViewSet,LoginView, LogoutView, CheckAuthenticatedView
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r"register/", SignupView)


urlpatterns = [
    path('authenticated/', CheckAuthenticatedView.as_view()),
    #path('register/', AccountsViewSet.as_view({'post': 'create'})),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    #path('delete/', DeleteAccountView.as_view()),
    #path('csrf_cookie/', GetCSRFToken.as_view())

]