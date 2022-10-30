from rest_framework import serializers
from .models import User, User_img, Auction, Auction_Receipt, Auction_result, Inform, Inform_cope, Alarm


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'address']


class AuctionCreateSerializerSupport(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['trust', 'name']


class AuctionCreateSerializer(serializers.ModelSerializer):
    make_user = AuctionCreateSerializerSupport()

    class Meta:
        model = Auction
        fields = ['id', 'title', 'img1', 'make_user', 'today_money']


class UserImgUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_img
        fields = ['img']


class AuctionDetailSerializer(serializers.ModelSerializer):
    make_user = serializers.IntegerField()

    class Meta:
        model = Auction
        fields = ['id', 'make_user', 'title', 'img1', 'img2', 'img3', 'img4', 'img5', 'content', 'start_money',
                  'today_money', 'auction_date', 'ship', 'ship_money']
        read_only_fields = ['id', 'make_user', 'today_money']


class AuctionDetailUserSerializer(serializers.ModelSerializer):
    auction_Receipt = AuctionDetailSerializer()

    class Meta:
        model = Auction_Receipt
        fields = ['id', 'auction_Receipt', 'money']


class AuctionReceiptListSerializer(serializers.ModelSerializer):
    user_Receipt = AuctionCreateSerializerSupport()

    class Meta:
        model = Auction_Receipt
        fields = ['user_Receipt', 'money', 'date']


class AuctionDetailUserNomelSerializer(serializers.ModelSerializer):
    user = AuctionCreateSerializerSupport()

    class Meta:
        model = User_img
        fields = ['user', 'img']


class AuctionDetaillUserAuctionList(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['img1']


class AuctionCreateSerializer2(serializers.ModelSerializer):
    auction_date = serializers.CharField()

    class Meta:
        model = Auction
        fields = ['title', 'img1', 'img2', 'img3', 'img4', 'img5', 'content', 'start_money',
                  'auction_date', 'ship', 'ship_money']


class InformListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inform
        fields = ['content_inform']


class AlarmUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ['title', 'content']