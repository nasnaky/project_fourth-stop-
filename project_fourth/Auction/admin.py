from django.contrib import admin
from .models import User, User_img, Auction, Auction_Receipt, Auction_result, Inform, Inform_cope, Alarm

admin.site.register(Alarm)
admin.site.register(Inform_cope)
admin.site.register(Inform)
admin.site.register(Auction_result)
admin.site.register(Auction_Receipt)
admin.site.register(Auction)
admin.site.register(User_img)
admin.site.register(User)
