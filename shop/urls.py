"""shop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path
urlpatterns = [
    path('shop/', views.homepage,name="home"), # 主页
    path('category/', views.category,name="category"), # 分类页面
    path('cart/', views.shoppingcart,name="cart"), # 购物车页面
    path('mine/', views.mine,name="mine"),  # 我的页面
    path('cglist/', views.get_cg_prod_list,name="cglist"), # 根据产品小类获取分类页面
    path('register/', views.register,name="register"), # 注册页面
    path('reg_username/', views.reg_username,name="reg_username"), # 注册验证username
    path('logout/', views.mylogout,name="logout"), # 注销
    path('login/', views.loginpage,name="login"), # 登陆
    path('updateToCart/<int:act>/', views.updateToCart,name="updateToCart"), # 更新购物车ajax
    path('cgsearch/', views.get_cglist_by_search,name="cgsearch"), # 根据搜索框获取分类页面
    path('checkout/', views.checkoutorder,name="checkout"), # 提交订单
    path('addressdetail/', views.addAddress,name="addressdetail"), # 详细地址
    path('addresslist/', views.address_list,name="addresslist"), # 地址列表
    path('updateAddress/<int:adsid>/', views.updateAddress,name="updateAddress"), # 更新地址
    path('deleteAddress/', views.deleteAddress,name="deleteAddress"), # 删除地址
    path('updatecoaddress/', views.updatecoaddress,name="updatecoaddress"), #  更新checkout的地址
    path('commitorder/', views.commitorder,name="commitorder"), #  提交订单

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
