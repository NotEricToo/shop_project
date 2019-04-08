# coding:utf-8
from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import JsonResponse
from shop.models import Recommend,Product,Category,User,Cart,UserAddress,Order,Comment,Prod_collect
from django.contrib.auth.hashers import make_password
import uuid,os
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from shop.mypaginator import MyPaginator
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
        cartlist = user.cart_set.filter(is_delete=False)
        orderlist = user.order_set.filter(is_delete=False)

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
    cid = request.GET.get("cid")
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
                if prod.prod_num > 0 :
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
                else:
                    # maxnum 表示已经超过最大库存
                    dict["status"] = "maxnum"
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
        refer_http = request.META.get("HTTP_REFERER")
        if request.method == "POST" :
            addressid = request.POST.get("addressid")
            adsname = request.POST.get("adsname")
            adsdetail = request.POST.get("adsdetail")
            adsrecname = request.POST.get("adsrecname")
            adsmphone = request.POST.get("adsmphone")
            referhttp = request.POST.get("referhttp")
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
                return redirect(referhttp)
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
        refer_http = request.META.get("HTTP_REFERER")
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

# 提交订单
def commitorder(request):

    token=request.session.get("token")
    dict={}
    try:
        user = User.objects.get(token=token)
        try:
            cartlist = Cart.objects.filter(user=user,is_delete=False)
            # 此处应该添加支付成功接口

            # === 先忽略
            adsid = request.GET.get("adsid")
            address = UserAddress.objects.get(id=adsid)
            paytype = request.GET.get("paytype")
            total_price = request.GET.get("total_price")
            ispay = True
            order = Order(user=user,address=address,pay_type=paytype,is_pay=ispay,order_price=total_price)
            order.save()
            cartlist.update(is_delete=True,order=order)
            for i in order.cart_set.all():
                # print(i.product.prod_id,i.product.prod_sales,i.prod_num)
                p = Product.objects.get(prod_id=i.product.prod_id)
                p.prod_sales =  p.prod_sales + i.prod_num
                p.prod_num = p.prod_num - i.prod_num
                p.save()


            dict["status"] = "success"
        except Exception as e :
            print(e)
            dict["status"] = "error"
    except User.DoesNotExist:
        dict["status"] = "nologin"
    return JsonResponse(dict)

# 订单列表页面
def orderlistpage(request):
    title = "订单列表"
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        orderlist = Order.objects.filter(is_delete=False,user = user ).order_by("-id")
        mp = MyPaginator(orderlist) # 5 个为一页
        orderlist = mp.getpage(1)
        nowpage = mp.nowpage
        totalpage = mp.totalpage
    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})
    return render(request, "shop/myorderlist.html", locals())

# 点击订单，获得订单详情
def orderlistdetail(request,orderid):
    if request.method == "GET":

        try:
            order = Order.objects.get(id = orderid)
            cartlist = order.cart_set.all()
            return render(request,"shop/function/orderlistdetail.html",locals())
        except Order.DoesNotExist as e :
            pass
    else:
        pass

# 点击订单列表 上一页 下一页， 获取相应的页数
def orderlist_getpage(request,nowpage,indicator):
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        orderlist = Order.objects.filter(is_delete=False, user=user).order_by("-id")
        mp = MyPaginator(orderlist,nowpage=nowpage)  # 5 个为一页
        # 1 表示 上一页
        if indicator == 1 :
            orderlist = mp.previous_page()

        # 2 表示下一页
        if indicator == 2 :
            orderlist = mp.next_page()

        nowpage = mp.nowpage
        totalpage = mp.totalpage

        return render(request,"shop/function/orderlistpage.html",locals())
    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})


#  product 详情页面：
def product_detail(request,prod_id):
    try:
        product = Product.objects.get(prod_id=prod_id)
        title=product.prod_name
        cartlist = Cart.objects.filter(is_delete=True,product=product).order_by("-id")[:5]
        commentlist = Comment.objects.filter(product = product)
        # 获取用户，并判断是否已经收藏该商品
        try:
            user = User.objects.get(token = request.session.get("token"))
            islogin = 1
            try:
                collect = Prod_collect.objects.get(user=user, product=product)
                iscollect = 1
            except Prod_collect.DoesNotExist as e:
                iscollect = 0
        except User.DoesNotExist as e:
            islogin = 0
            iscollect = 0
        mp = MyPaginator(commentlist)  # 5 个为一页
        commentlist = mp.getpage(1)
        nowpage = mp.nowpage
        totalpage = mp.totalpage
        return render(request, "shop/product.html", locals())
    except Product.DoesNotExist as e:
        pass

# comment 添加页
def comment_page(request,prod_id):
    prod = Product.objects.get(prod_id=prod_id)
    title = "评价商品："
    token = request.session.get("token")
    try:
        user = User.objects.get(token=token)
        httpreferer = request.META.get("HTTP_REFERER")
        return render(request, "shop/addcomment.html", locals())
    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})


# 添加 comment 转商品页面
def commit_comment(request):
    token = request.session.get("token")
    try:
        user = User.objects.get(token = token )
        content = request.GET.get("content")
        prod_id = request.GET.get("prod_id")
        httpreferer = request.GET.get("httpreferer")
        product = Product.objects.get(prod_id = prod_id)
        comment = Comment(user = user , product = product , content= content)
        comment.save()
        return redirect(httpreferer)
    except User.DoesNotExist as e:
        pass


# 收藏商品
def collectproduct(request):

    token = request.session.get("token")
    prod_id = request.GET.get("prod_id")
    product = Product.objects.get(prod_id=prod_id)
    try:
        user = User.objects.get(token = token)
        try:
            collect_list = Prod_collect.objects.filter(user=user,product=product )
            if collect_list.count() == 0 :
                collect = Prod_collect(user=user, product=product)
                collect.save()
                return render(request, "shop/function/collected_product.html", locals())
            else :
                collect_list.delete()
                return render(request,"shop/function/no-collected_product.html",locals())

        except Exception as e:
            print(e)

    except User.DoesNotExist as e:
        pass

# 商品详情页， 添加购物车
def addtocart_prodpage(request):
    token = request.session.get("token")
    dict = {}
    try:
        user = User.objects.get(token = token)
        prod_id = request.GET.get("prod_id")
        product = Product.objects.get(prod_id=prod_id)

        prod_num = int(request.GET.get("prod_num"))
        # print(prod_num)
        cart = Cart.objects.get(user=user,product=product,is_delete=False)
        try:

            cart.prod_num = cart.prod_num + prod_num
            if cart.prod_num <= product.prod_num :
                cart.save()
            else:
                raise Exception
            dict["status"] = "success"
        except Exception as e:
            print(e)
            dict["status"] = "error"
    except User.DoesNotExist :
        dict["status"] = "nologin"
    except Cart.MultipleObjectsReturned as e:
        dict["status"] = "error"
    except Cart.DoesNotExist as e:
        if prod_num<=product.prod_num:
            cart = Cart(user=user, product=product, prod_num=prod_num)
            cart.save()
            dict["status"] = "success"
        else:
            dict["status"] = "error"

    return JsonResponse(dict)

# 我的收藏
def my_collect(request,userid):
    title = "我的收藏"
    try:
        user = User.objects.get(id=userid)
        collectlist = Prod_collect.objects.filter(user=user)
        mp = MyPaginator(collectlist)
        collectlist = mp.getpage(1)
        return render(request,"shop/prod_collect.html",locals())
    except User.DoesNotExist as e:
        return render(request, "shop/login.html", {"title": "请登陆"})


# 删除我的收藏
def del_collect(request):
    prod_id = request.GET.get("prod_id")
    product = Product.objects.get(prod_id = prod_id)
    token = request.session.get("token")
    dict={}
    try:
        user = User.objects.get(token = token)
        try:
            collect = Prod_collect.objects.get(user=user,product=product)
            collect.delete()
            dict["status"] = "success"
        except Exception as e:
            pass
    except User.DoesNotExist as e:
        dict["status"] = "nologin"
    return JsonResponse(dict)
