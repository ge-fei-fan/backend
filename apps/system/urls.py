from rest_framework import routers
from apps.system.views.cat import CatViewSet, WeightViewset
from apps.system.views.daily import DailyViewSet
from apps.system.views.file_list import FileViewSet
from apps.system.views.pay import PayViewSet



system_url = routers.SimpleRouter()
system_url.register(r'cat', CatViewSet)
system_url.register(r'weight', WeightViewset)
system_url.register(r'daily', DailyViewSet)
system_url.register(r'file', FileViewSet)
system_url.register(r'pay', PayViewSet)

urlpatterns = []
urlpatterns += system_url.urls

