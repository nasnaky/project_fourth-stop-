from django.urls import path, include
from rest_framework import routers

from django.conf.urls.static import static
from django.conf import settings

from .views import create_user, login, logout, search, User_img_update, changeName, addMoney, move, check_password \
    , change_password, aution_list, aution_detail, auction_re_list, auction_participation, auction_detail_nomel,\
    auction_detail_auction_list, create_auction, Inform_list_and_create, Alarm_list

routers1 = routers.DefaultRouter()
routers1.register('', User_img_update, basename='User_img')

routers2 = routers.DefaultRouter()
routers2.register('', create_auction, basename='create_auction')

urlpatterns = [
    path('CUS/', create_user),
    path('user_img/', include(routers1.urls)),
    path('COB/', include(routers2.urls)),
    path('CNA/', changeName),
    path('bank/', addMoney),
    path('mv/', move),
    path('CPW/', check_password),
    path('CPW/C/', change_password),
    path('login/', login),
    path('logout/', logout),
    path('search=<str:search_text>', search),
    path('list/', aution_list),
    path('ob/<int:pk>', aution_detail),
    path('ob/re/<int:pk>', auction_re_list),
    path('ob/us/<int:pk>', auction_detail_nomel),
    path('ob/usob/<int:pk>', auction_detail_auction_list),
    path('APT/<int:pk>', auction_participation),
    path('ifm/<int:pk>',Inform_list_and_create),
    path('alm/',Alarm_list)
]
urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
