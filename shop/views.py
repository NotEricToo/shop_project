# coding:utf-8
from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import JsonResponse
from shop.models import Recommend,Product,Category,User,Cart,UserAddress
from django.contrib.auth.hashers import make_password
import uuid,os
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

from django.http import request

def global_view(request):
    http_referer = request.META.get('HTTP_REFERER', 'Not defined')
    return locals()


def homepage(request):
    title="EricBuy首页"
    rec = Recommend.objects.all().order_by("-id")[:4]
    cglist = Category.objects.all().order_by("-rem_order")
    # 验证是否登陆，登陆的话显示图片
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
    except Exception as e:
        # user = {"user_img":"shop/default/img1.jpg"}
        pass
    return render(request,'shop/index.html',locals())

# 根据login 状态重置 prodlist 的值为购物车中的值  ：
def getCartProdlist(request,prodlist):
    token = request.session.get("token")
    prodlist2 = []
    try:
        user = User.objects.get(token=token)
        for prod in prodlist:
            try:
                cart = Cart.objects.get(user=user,is_delete=False,product=prod)
                prod.cartnum = cart.prod_num
            except Cart.DoesNotExist as e:
                prod.cartnum = 0
            prodlist2.append(prod)
    except User.DoesNotExist as e:
        # 没登陆， 把所有数字都默认为 0
        for prod in prodlist:
            prod.cartnum = 0
            prodlist2.append(prod)
    prodlist = prodlist2
    return prodlist

def category(request):
    title="分类"
    cglist = Category.objects.all().order_by("-rem_order")
    prodlist = Product.objects.all()[:4]
    prodlist = getCartProdlist(request,prodlist) # 处理初始化的产品数


    return render(request,'shop/category.html',locals())

# 根据分类获取产品列表
def get_cg_prod_list(request):

    sub          = request.GET.get("sub_id",None)
    searchText   = request.GET.get("searchText", None)
    type         = request.GET.get("type",0)
    print("==",type,"===",searchText)
    try:
        if type == "0":
            prodlist = Product.objects.filter(prod_cg__id=sub)
        elif type == "1":
            prodlist = Product.objects.filter(prod_name__contains=searchText)

        if prodlist.count() == 0 :
            return render(request, 'shop/function/productNotFound.html', {})
        prodlist = getCartProdlist(request, prodlist)  # 处理初始化的产品数
        # category_listprod.html 该页面就是产品列表页面
        return render(request, 'shop/function/category_listprod.html', {"prodlist": prodlist})
    except Product.DoesNotExist:
        return render(request, 'shop/function/productNotFound.html', {})

def get_cglist_by_search(request):
    searchText = request.GET.get("searchText",None)

    try:
        prodlist = Product.objects.filter(prod_name__contains=searchText)
        prodlist = getCartProdlist(request, prodlist)  # 处理初始化的产品数
        # category_listprod.html 该页面就是产品列表页面
        return render(request, 'shop/function/category_listprod.html', {"prodlist": prodlist})
    except Product.DoesNotExist as e:
        pass


# 购物车页面
def shoppingcart(request):
    title="购物车"
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        cartlist = Cart.objects.filter(user=user,is_delete=False)
        totalprice = 0
        for item in cartlist:
            totalprice += item.prod_num*item.product.prod_price
        return render(request, "shop/shoppingcart.html", locals())
    except User.DoesNotExist as e:
        return loginpage(request)

# 我的页面
def mine(request):
    title = "我的"
    token = request.session.get("token")
    try:
        user = User.objects.get( token = token )

    except User.DoesNotExist as e:
        return loginpage(request)
    return render(request, "shop/user.html", locals())

# 用户注册
def register(request):
    title="用户注册"
    if request.method == "POST":

        username = request.POST.get("username")
        password = make_password(request.POST.get("password"))
        email = request.POST.get("email")
        phonenum = request.POST.get("phonenumber")
        userimg = request.FILES['userimg']
        # 头像文件保存
        # filepath = os.path.join(settings.MEDIA_ROOT,"userimg",uuid.uuid4().hex+".jpg")
        filename = uuid.uuid4().hex+".jpg"
        filepath = os.path.join(settings.MEDIA_ROOT,filename)
        urlpath = os.path.join(settings.MEDIA_URL,filename)
        f2 = open(filepath,"wb")

        for item in userimg.chunks():
            f2.write(item)
        f2.close()

        token = uuid.uuid4().hex
        user = User.create(username=username,email=email,password=password,phone_num=phonenum,user_img=urlpath,token=token)
        user.save()
        request.session["token"] = token
        return redirect(reverse("login"))
    return render(request,"shop/reg.html",locals())

# 验证注册用户名
def reg_username(request):
    username = request.GET.get("username")
    dict=  {}
    try:
        user = User.objects.get(username=username)
        dict["status"] = "error"
    except User.DoesNotExist as e:
        dict["status"] = "success"
    return JsonResponse(dict)

# 登陆 页面
@csrf_exempt
def loginpage(request):
    title = "登陆"
    if request.method == "POST":
        dict={}
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            if check_password(password,user.password):

                # 验证成功
                # 保存session，返回上一页
                dict["status"]="success"
                dict["page"] = request.META.get("HTTP_REFERER","/mine/")
                request.session["token"] = user.token
            else:
                # 返回密码错误
                dict["status"] = "error"

        except User.DoesNotExist as e:
            dict["status"] = "error"
        # 最终都返回 这个状态的 dictionary
        return JsonResponse(dict)
    return render(request, "shop/login.html", locals())


# 注销 logout
def mylogout(request):
    logout(request)
    return redirect("/shop/")

# 分类页面，把商品添加或减少到购物车
def updateToCart(request,act):
    # act 为操作步骤， 1 添加 0 减少
    dict = {}
    # 获取产品id
    prodid = request.GET.get("prodid")
    prod = Product.objects.get(prod_id = prodid)
    sumprice = 0
    # 根据 token， 判断用户是否已经登陆
    # 已登录，获取用户
    token = request.session.get("token",None)
    if token :
        try:
            user = User.objects.get(token = token)
            try:
                # 在购物车，获取购物车记录。
                # dict 加入加1后的产品数量。
                # 获取购物车数据条件：
                # 该用户下的， 未被删除的， 含有该产品的
                cart = Cart.objects.get(user = user,is_delete=False,product = prod)
                # 1 添加
                if act == 1:
                    if cart.prod_num < prod.prod_num :
                        # 购物车该产品数量<库存，则 加 1，否则，直接返回 status =  maxnum。
                        cart.prod_num += 1
                        cart.save()

                        dict["status"] = "success"
                        dict["num"] = cart.prod_num
                    else:
                        # maxnum 表示已经超过最大库存
                        dict["status"] = "maxnum"
                # 0 为减少
                elif act == 0:
                    if cart.prod_num == 0 :
                        dict["status"] = "error"
                    else :
                        cart.prod_num -= 1
                        cart.save()
                        dict["num"] = cart.prod_num
                        if cart.prod_num == 0 :
                            cart.delete()
                        dict["status"] = "success"
                elif act == 2 :
                    # act 为  2 ， 直接删除掉 Cart 表中该产品对应的信息
                    cart.delete()
            except Cart.DoesNotExist as e :
                #不在购物车， 直接添加一条新的记录
                if act == 1:
                    # 1 添加
                    # 该用户购物车没有该产品，新增
                    cart = Cart(user = user, product = prod)
                    cart.save()
                    dict["status"] = "success"
                    dict["num"] = cart.prod_num
                elif act == 0 :
                    # 0 为减少
                    dict["status"] = "error"
            finally:
                # 最后，获取该用户现有的购物车所有个数和总价
                cartlist = Cart.objects.filter(user=user, is_delete=False)
                dict["totalnum"] = cartlist.count()
                totalprice = 0
                for item in cartlist:
                    totalprice += item.product.prod_price * item.prod_num
                dict["totalprice"] = round(totalprice, 2)
        except User.DoesNotExist as e:
            # 如果未登陆
            dict["status"] = "nologin"
    # 未登陆， 直接返回 nologin， 然后页面直接跳到 login 页面（在javascript 中进行跳转）
    else:
        dict["status"] = "nologin"


    return JsonResponse(dict)


# 地址添加页面
def addAddress(request):
    title="收货地址"
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        if request.method == "POST" :
            addressid = request.POST.get("addressid")
            adsname = request.POST.get("adsname")
            adsdetail = request.POST.get("adsdetail")
            adsrecname = request.POST.get("adsrecname")
            adsmphone = request.POST.get("adsmphone")
            try:
                # 如果存在该 address ， 就更新
                useraddress = UserAddress.objects.get(id=addressid)

                useraddress.addressname = adsname
                useraddress.address = adsdetail
                useraddress.receive_name = adsrecname
                useraddress.receive_phone = adsmphone
                useraddress.save()

            except UserAddress.DoesNotExist as e:
                # 不存在， 就新加
                address = UserAddress(addressname=adsname, user=user, receive_name=adsrecname,
                                      receive_phone=adsmphone,
                                      address=adsdetail)
                address.save()
            finally:
                return redirect(reverse("addresslist"))
    except User.DoesNotExist as e:
        return render(request,"shop/login.html",{"title":"请登陆"})
    return render(request,"shop/addressInfoDetail.html",locals())

# 提交订单页面
def checkoutorder(request):
    title = "提交订单"
    token = request.session.get("token")
    total_price = 0
    try:
        user = User.objects.get(token=token)
        addresslist = UserAddress.objects.filter(user=user)
        cartlist = Cart.objects.filter(user=user, is_delete=False)
        for item in cartlist:
            total_price += item.prod_num*item.product.prod_price
    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})
    return render(request, "shop/checkout.html", locals())


# 我的详细信息
def mydetailinfo(request):
    title="我的详细信息"
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)


    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})
    return render(request,"shop/mydetailinfo.html",locals())

# 地址列表页面：
def address_list(request):
    title = "地址列表"
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        addresslist = UserAddress.objects.filter(user=user)


    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})
    return render(request, "shop/address_list.html", locals())


# 地址更新页面
def updateAddress(request,adsid):
    title = "地址更新"
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        try:
            address = UserAddress.objects.get(id=adsid)
            return render(request,"shop/addressInfoDetail.html",locals())
        except UserAddress :
            pass
            # return 404 not found
    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})

# 删除地址
def deleteAddress(request):
    adsid = request.GET.get("adsid")
    dict={}
    try:
        address = UserAddress.objects.get(id=adsid)
        address.delete()
        dict["status"]="success"
    except UserAddress.DoesNotExist :
        dict["status"] = "error"
    return JsonResponse(dict)

# ajax 更新 co 的地址
def updatecoaddress(request):
    adsid = request.GET.get("adsid")
    try:
        address = UserAddress.objects.get(id=adsid)
        return render(request,"shop/function/checkout-address.html",locals())
    except UserAddress.DoesNotExist :
        pass