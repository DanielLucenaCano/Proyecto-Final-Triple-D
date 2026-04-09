from django.urls import path

from apps.servers.views import (
    PriceCalculatorView,
    ServerCollectionView,
    ServerDetailView,
    ServerStartView,
    ServerStopView,
)

urlpatterns = [
    path('', ServerCollectionView.as_view(), name='server-list-create'),
    path('configurator/price/', PriceCalculatorView.as_view(), name='server-price-calculator'),
    path('<int:server_id>/', ServerDetailView.as_view(), name='server-update'),
    path('<int:server_id>/start/', ServerStartView.as_view(), name='server-start'),
    path('<int:server_id>/stop/', ServerStopView.as_view(), name='server-stop'),
]
