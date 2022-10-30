import hashlib

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from django.db.models import Q
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from django.utils import timezone

from .models import User, User_img, Auction, Auction_Receipt, Auction_result, Inform, Inform_cope, Alarm
from .serializers import UserCreateSerializer, AuctionCreateSerializer, UserImgUpdateSerializer, AuctionDetailSerializer \
    , AuctionReceiptListSerializer, AuctionDetailUserSerializer, AuctionDetailUserNomelSerializer, \
    AuctionDetaillUserAuctionList, AuctionCreateSerializer2, InformListSerializer, AlarmUserListSerializer


def date_check():
    lists = Auction.objects.filter(Q(auction_date__range=[datetime.today() - timedelta(days=365), datetime.today()])
                                   & Q(check_date=False))
    for o in lists:
        Auction_check.end_auction(o)
        o.check_date = True
        o.save()


class end_auction_play:

    def money_back(self):
        user = self.user_Receipt
        user.bank = user.bank + self.money
        user.save()


class Auction_check:
    def end_auction(self):
        lists = Auction_Receipt.objects.filter(auction_Receipt=self)
        for o in lists:
            if self.today_money != o.money:
                end_auction_play.money_back(o)
                o.result = False
                o.save()
            else:
                o.result = True
                o.save()
                objects = Auction_result()
                objects.user_result = o.user_Receipt
                objects.auction_result = o.auction_Receipt
                objects.address = o.user_Receipt.address
                objects.save()
                odjected = o.auction_Receipt
                doing = Alarm()
                doing.user_alarm = odjected.make_user
                doing.content = "경매가 종료됐습니다."
                doing.content = odjected.title + "의 경매가 종료되었습니다. 경매 낙찰자의 주소는 " + objects.address + "입니다." \
                                                                                                   "자세한 내용은 결과 화면을 참고해 주세요"
                doing.save()


class check:
    def email_check(self):
        try:
            email = User.objects.get(email=self)
            return False
        except Exception:
            return True

    def token_check(self):
        date_check()

        token = self.META.get('HTTP_TOKEN')
        try:
            user = User.objects.get(token=token)
            if user.token_max_date <= timezone.now():
                return False
            return True
        except Exception:
            return token

    def password_check(self):
        token = self.META.get('HTTP_TOKEN')
        user = User.objects.get(token=token)
        data = JSONParser().parse(self)
        password = data['password']
        password = hashlib.sha256(password.encode())
        password = str(password.hexdigest())
        if user.password == password:
            return True
        return False


@api_view(['POST'])  # 회원 가입
def create_user(request):
    if request.method == "POST":
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            if check.email_check(email):
                email_name = email.split('@')
                name = email_name[0]
                password = serializer.validated_data.get("password")
                password = hashlib.sha256(password.encode())
                serializer.save(name=name, password=str(password.hexdigest()))
                img = User_img()
                img.user = User.objects.get(email=email)
                img.save()
                return Response({
                    "message": "회원 가입이 완료됐습니다."
                }, status=status.HTTP_201_CREATED)
            return Response({
                "message": "중복된 이메일입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "잘못된 요청입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])  # 로그인
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            email_user = User.objects.get(email=data['email'])
            password = data['password']
            password = hashlib.sha256(password.encode())
            password = str(password.hexdigest())
            if email_user.password == password:
                tokenData = data['email'] + str(datetime.today())
                tokenHash = hashlib.sha1(tokenData.encode())
                token = str(tokenHash.hexdigest())
                email_user.token = token
                email_user.token_max_date = datetime.today() + timedelta(days=10)
                email_user.save()
                return Response({
                    "token": token
                })
            return Response({
                "message": "비밀 번호가 틀렸습니다."
            })
        except Exception:
            return Response({
                "message": "잘못된 이메일입니다."
            })


class User_img_update(viewsets.ModelViewSet):
    serializer_class = UserImgUpdateSerializer
    queryset = User_img.objects.all()

    def update(self, request, *args, **kwargs):
        if check.token_check(request):
            data = request.data
            token = request.META.get('HTTP_TOKEN')
            user = User.objects.get(token=token)
            old_data = User_img.objects.get(user=user)
            old_data.img = data['img']
            old_data.save()
            return Response({
                "message": "변경됐습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })


@api_view(['GET'])  # 로그아웃
def logout(request):
    if request.method == "GET":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            user = User.objects.get(token=token)
            user.token_max_date = datetime.today() - timedelta(days=10)
            user.save()
            return Response({
                "message": "로그아웃 됬습니다."
            })
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })


@api_view(['GET'])  # 검색
def search(request, search_text):
    if request.method == "GET":
        lists = Auction.objects.filter(Q(check_date=False) & Q(title__contains=search_text))
        serializer = AuctionCreateSerializer(lists, many=True)
        return Response(serializer.data)


@api_view(['POST'])  # 이름 변경
def changeName(request):
    if request.method == "POST":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            data = JSONParser().parse(request)
            user = User.objects.get(token=token)
            user.name = data['name']
            user.save()
            return Response({
                "message": "이름변경이 완료되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })


@api_view(['POST'])  # 충전
def addMoney(request):
    if request.method == "POST":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            data = JSONParser().parse(request)
            user = User.objects.get(token=token)
            user.bank += data['money']
            user.save()
            return Response({
                "message": "충전이 완료되었습니다."
            }, status=status.HTTP_200_OK)


@api_view(['POST'])  # 주소 변경
def move(request):
    if request.method == "POST":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            data = JSONParser().parse(request)
            user = User.objects.get(token=token)
            user.address += data['address']
            user.save()
            return Response({
                "message": "주소가 변경되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })


@api_view(['POST'])  # 비밀번호 확인
def check_password(request):
    if request.method == "POST":
        if check.token_check(request):
            if check.password_check(request):
                return Response({
                    "result": True
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "비밀번호가 틀렸습니다."
            })
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })


@api_view(['POST'])  # 비밀번호 변경
def change_password(request):
    if request.method == "POST":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            user = User.objects.get(token=token)
            data = JSONParser().parse(request)
            password = data['password']
            password = hashlib.sha256(password.encode())
            password = str(password.hexdigest())
            user.password = password
            return Response({
                "message": "비밀번호가 변경되었습니다."
            })


@api_view(['GET'])  # 최근 5개 경매 받기
def aution_list(request):
    if request.method == "GET":
        list = Auction.objects.order_by("-pk")[:5]
        list = AuctionCreateSerializer(list, many=True)
        return Response(list.data)


@api_view(['GET'])  # 디테일 경매 정보
def aution_detail(request, pk):
    if request.method == "GET":
        token = request.META.get('HTTP_TOKEN')
        try:
            user = User.objects.get(token=token)
            auction = Auction.objects.get(pk=pk)
            objects = Auction_Receipt.objects.get(Q(user_Receipt=user) & Q(auction_Receipt=auction))
            serializer = AuctionDetailUserSerializer(objects)
            return Response(serializer.data)
        except Exception:
            pass
        objects = Auction.objects.get(pk=pk)
        serializer = AuctionDetailSerializer(objects)
        return Response(serializer.data)


@api_view(['GET'])  # 경매 목록
def auction_re_list(request, pk):
    if request.method == "GET":
        objects = Auction.objects.get(pk=pk)
        lists = Auction_Receipt.objects.filter(auction_Receipt=objects).order_by("-money")
        serilaizer = AuctionReceiptListSerializer(lists, many=True)
        return Response(serilaizer.data)


@api_view(['POST'])  # 경매 참여
def auction_participation(request, pk):
    if request.method == "POST":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            data = JSONParser().parse(request)
            user = User.objects.get(token=token)
            objects = Auction.objects.get(pk=pk)
            money = data['money']
            try:
                old_part = Auction_Receipt.objects.get(Q(user_Receipt=user) & Q(auction_Receipt=objects))
                old_money = old_part.money
                if user.bank < money - old_money:
                    return Response({
                        "message": "계정의 자금이 부족합니다."
                    })
                minus = money - old_money
                user.bank = user.bank - minus
                old_part.money = money
                user.save()
                old_part.save()
            except Exception:
                pass
            if user.bank < money:
                return Response({
                    "message": "계정의 자금이 부족합니다."
                })
            user.bank = user.bank - money
            saved = Auction_Receipt()
            saved.user_Receipt = user
            saved.auction_Receipt = objects
            saved.money = money
            if objects.today_money < money:
                objects.today_money = money
                objects.save()
            user.save()
            saved.save()
            return Response({
                "message": "참여 됐습니다."
            })
        return Response({
            "message": "다시 로그인해 주세요"
        })


@api_view(['GET'])  # 디테일 유저 정보
def auction_detail_nomel(request, pk):
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        img = User_img.objects.get(user=user)
        serializer = AuctionDetailUserNomelSerializer(img)
        return Response(serializer.data)


@api_view(['GET'])  # 디테일 유저 판매 리스트
def auction_detail_auction_list(request, pk):
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        objects = Auction.objects.filter(make_user=user)
        serializer = AuctionDetaillUserAuctionList(objects, many=True)
        return Response(serializer.data)


class create_auction(viewsets.ModelViewSet):
    serializer_class = AuctionCreateSerializer2
    queryset = Auction.objects.all()

    def create(self, request):
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            user = User.objects.get(token=token)
            serializer = AuctionCreateSerializer2(data=request.data)
            if serializer.is_valid():
                money = serializer.validated_data.get('start_money')
                serializer.save(make_user=user, today_money=money)
                return Response({
                    "message": "생성 완료 되었습니다."
                })
            return Response(serializer.errors)
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })


@api_view(['GET', 'POST'])  # 신고 리스트, 저장
def Inform_list_and_create(request, pk):
    if request.method == "POST":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            data = JSONParser().parse(request)
            user = User.objects.get(token=token)
            objects = Auction.objects.get(pk=pk)
            message = data['message']
            inform = Inform()
            inform.user_inform = user
            inform.auction_inform = objects
            inform.user_by_inform = objects.make_user
            inform.content_inform = message
            inform.save()
            return Response({
                "message": "신고 접수 되었습니다."
            })
        return Response({
            "message": "다시 로그인해 주시길 바랍니다."
        })
    if request.method == "GET":
        if check.token_check(request):  # 이후 어드민 확인으로 교체
            list = Inform.objects.order_by("-pk")[:pk]
            serializer = InformListSerializer(list, many=True)
            return Response(serializer.data)


@api_view(['GET'])  # 알람 리스트
def Alarm_list(request):
    if request.method == "GET":
        if check.token_check(request):
            token = request.META.get('HTTP_TOKEN')
            user = User.objects.get(token=token)
            listed = Alarm.objects.filter(user_alarm=user).order_by("-pk")
            for i in listed:
                i.check_see = True
                i.save()
            serializer = AlarmUserListSerializer(listed, many=True)
            return Response(serializer.data)

