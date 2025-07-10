from django.urls import path
from .views import BecomeProfessionalView, list_professionals, HireProfessionalView

urlpatterns = [
    path('professionals/', BecomeProfessionalView.as_view(), name='become-professional'),
    path('professionalslist/', list_professionals, name='list-professionals'),
    path('hire/', HireProfessionalView.as_view(), name='hire-professional'),
]