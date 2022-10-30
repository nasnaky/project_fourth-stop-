from django.db import models


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=128)
    address = models.TextField()
    name = models.TextField()
    bank = models.IntegerField(default=0)
    trust = models.IntegerField(default=75)
    token = models.TextField(null=True, blank=True)
    token_max_date = models.DateTimeField(null=True, blank=True)
    admin = models.BooleanField(default=False)

    def __int__(self):
        return self.id


class User_img(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='user/', default='user/default')


class Auction(models.Model):
    make_user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.TextField()
    img1 = models.ImageField(upload_to='Auction/')
    img2 = models.ImageField(upload_to='Auction/', blank=True, null=True)
    img3 = models.ImageField(upload_to='Auction/', blank=True, null=True)
    img4 = models.ImageField(upload_to='Auction/', blank=True, null=True)
    img5 = models.ImageField(upload_to='Auction/', blank=True, null=True)
    content = models.TextField()
    start_money = models.IntegerField()
    today_money = models.IntegerField(null=True, blank=True)
    auction_date = models.DateTimeField()
    ship = models.TextField()
    ship_money = models.IntegerField(default=0)
    check_date = models.BooleanField(default=False)


class Auction_Receipt(models.Model):
    user_Receipt = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_Receipt = models.ForeignKey(Auction, on_delete=models.CASCADE)
    money = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField(blank=True, null=True)


class Auction_result(models.Model):
    auction_result = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user_result = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.address = models.TextField()


class Alarm(models.Model):
    user_alarm = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    check_see = models.BooleanField(default=False)


class Inform(models.Model):
    user_inform = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_inform')
    user_by_inform = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_by_inform')
    auction_inform = models.ForeignKey(Auction, on_delete=models.CASCADE)
    content_inform = models.TextField()
    check_result = models.BooleanField(default=False)


class Inform_cope(models.Model):
    by_inform = models.ForeignKey(Inform, on_delete=models.CASCADE)
    deletes = models.BooleanField(blank=True,null=True)
    minus = models.IntegerField(default=0)
    passed = models.BooleanField(blank=True, null=True)
    content = models.TextField()