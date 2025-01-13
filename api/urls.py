from django.urls import path, include


urlpatterns = [
    path('account/', include('account.urls')),
    path('v1/', include('prompt.urls'))
]
