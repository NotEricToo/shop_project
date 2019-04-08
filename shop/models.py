# coding:utf-8
from django.db import models
import datetime
import uuid
# Create your models here.
#
# def image_upload_to(instance, filename):
#     return 'img/{Y}/{m}/{d}/{uuid}{filename}'.format(Y=datetime.datetime.now().strftime('%Y'),
#                                                            m=datetime.datetime.now().strftime('%m'),
#                                                            d=datetime.datetime.now().strftime('%d'),
#                                                            uuid=uuid.uuid4().hex, filename=filename)
def upload_to(instance,filename):
    filename = datetime.datetime.now().strftime('%Y') + "/" + datetime.datetime.now().strftime('%m') + "/" + \
                datetime.datetime.now().strftime('%d')  + "/" + uuid.uuid4().hex + ".jpg"
    return filename


'''
轮滑推荐： 4 张图片
Recommend:
id
img
name
'''
class Recommend(models.Model):
    id = models.AutoField(primary_key=True)
    # img = models.ImageField(upload_to="rec",verbose_name="首页滚轮图片")
    img = models.ImageField(upload_to=upload_to,verbose_name="首页滚轮图片")
    name = models.CharField(max_length=50,blank=False,null=False,verbose_name="图片名字")
    class Meta:
        db_table = "tbl_recommend"
        verbose_name_plural="首页轮播推荐表"


'''
首页：
推荐的内容：
根据分类进行推荐

大分类：
category :
id
cg_name
create_date
rem_order -- 推荐的 等级， order 值越大，越前面
'''

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=20,blank=False,null=False,verbose_name="大类名字")
    create_date=models.DateField(default=datetime.datetime.now)
    rem_order = models.IntegerField(verbose_name="推荐等级",default=0)

    def __str__(self):
        return self.cg_name

    class Meta:
        db_table="tbl_category"
        # verbose_name="商品大类表"
        verbose_name_plural = "商品大类表"

'''
小分类：
sub_category
id
cg_name
category
create_date
'''
class Sub_category(models.Model):
    id = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=20, blank=False, null=False, verbose_name="小类名字")
    create_date = models.DateField(default=datetime.datetime.now )
    category = models.ForeignKey(Category,verbose_name="所属大类",on_delete=False)

    def __str__(self):
        return self.cg_name


    class Meta:
        db_table="tbl_sub_category"
        verbose_name_plural="商品小类表"

'''
user
id
username
email
password
token
create_date
chinese_name
phone_num
desc
user_img - 用户头像
'''

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,null=False,blank=False,verbose_name="用户名")
    email=models.EmailField(null=True,blank=True,verbose_name="邮件")
    password = models.CharField(max_length=200,blank=False,null=False,verbose_name="密码")
    token = models.CharField(max_length=50,blank=True,null=True)
    create_date=models.DateField(default=datetime.datetime.now)
    chinese_name=models.CharField(max_length=50,null=True,blank=True,verbose_name="中文名字")
    phone_num = models.CharField(max_length=20,null=False,blank=False,verbose_name="电话号码")
    desc = models.TextField(max_length=200,null=True,blank=True,verbose_name="个人描述")
    user_img = models.ImageField(upload_to=upload_to,default="userimg/blank.png",max_length=200)
    class Meta:
        db_table="tbl_user"
        verbose_name_plural="个人用户表"

    @classmethod
    def create(cls,username,email,password,token,phone_num,user_img):

        user = cls(username=username,
                   email=email,
                   password=password,
                   token=token,
                   phone_num=phone_num,
                   user_img=user_img
                   )
        return user

'''
product
prod_id
prod_name
prod_longname
prod_img -- 主要显示的 img
prod_rollimg1 -- 用于详情页轮播的img
prod_rollimg2 -- 用于详情页轮播的img
prod_rollimg3 -- 用于详情页轮播的img
prod_rollimg4 -- 用于详情页轮播的img
prod_desc  - 描述
prod_price  - 单价
prod_num - 库存
prod_brand -- 品牌
prod_cg -- 商品分类:属于小类
prod_sales -- 销量
is_delete - boolean - 是否已删除
'''

class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=20,null=False,blank=False,verbose_name="商品名字")
    prod_longname = models.TextField(max_length=100,null=False,blank=False,verbose_name="商品长名字")
    prod_img = models.ImageField(upload_to=upload_to,verbose_name="商品图片")
    prod_rollimg1 = models.ImageField(upload_to=upload_to,blank=True,null=True,verbose_name="商品轮播图")
    prod_rollimg2 = models.ImageField(upload_to=upload_to,blank=True,null=True,verbose_name="商品轮播图2")
    prod_rollimg3 = models.ImageField(upload_to=upload_to,blank=True,null=True,verbose_name="商品轮播图3")
    prod_rollimg4 = models.ImageField(upload_to=upload_to,blank=True,null=True,verbose_name="商品轮播图4")
    prod_desc = models.TextField(max_length=200,null=True,blank=True,verbose_name="商品描述")
    prod_price = models.FloatField(null=False,blank=False,verbose_name="单价")
    prod_num = models.IntegerField(default=0,verbose_name="库存")
    prod_brand = models.CharField(max_length=20,null=True,blank=True,verbose_name="商品品牌")
    prod_cg = models.ForeignKey(Sub_category,on_delete=False,null=True,blank=True,verbose_name="商品分类(小类)")
    prod_sales = models.IntegerField(default=0,verbose_name="总销量")
    is_delete = models.BooleanField(default=False,verbose_name="已删除")

    def show_category(self):
        return self.prod_cg.category.cg_name

    class Meta:
        db_table="tbl_product"
        verbose_name_plural="商品表"


'''

地址表
address
id
receive_name
receive_phone
address
create_date
update_date
'''

class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)
    addressname = models.CharField(max_length=20,null=True,blank=True,verbose_name="地址名称")
    user = models.ForeignKey(User,on_delete=False,blank=True,null=True,verbose_name="用户")
    receive_name = models.CharField(max_length=20,null=False,blank=False,verbose_name="收货人名字")
    receive_phone = models.CharField(max_length=20,null=False,blank=False,verbose_name="收货人电话")
    address = models.TextField(max_length=200,null=False,blank=False,verbose_name="收货地址")
    create_date = models.DateTimeField(default=datetime.datetime.now)
    update_date = models.DateTimeField(default=datetime.datetime.now,verbose_name="最新更新时间")
    class Meta:
        db_table="tbl_address"
        verbose_name_plural="收货地址表"


'''

order
id
user
create_date
address
pay_type -- 1 微信 2  支付宝 
is_pay  
is_delete
'''
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    # orderid = models.CharField(max_length=20,null=False,blank=False,verbose_name="订单号",unique=True)
    user = models.ForeignKey(User,on_delete=False,verbose_name="用户")
    create_date = models.DateField(default=datetime.datetime.now)
    address = models.ForeignKey(UserAddress,on_delete=False,verbose_name="收货信息")
    pay_type = models.CharField(max_length=20,null=True,blank=True,verbose_name="支付方式")
    is_pay = models.BooleanField(default=False,verbose_name="是否已支付")
    order_price = models.FloatField(default=0,verbose_name="订单总价")
    is_delete = models.BooleanField(default=False,verbose_name="已删除")
    class Meta:
        db_table="tbl_order"
        verbose_name_plural="订单表"

'''
cart 购物车表
id
user
order -- default - 0
prod_id
prod_num -- 已加入购物车数量
create_date
is_delete -- boolean
'''
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=False,verbose_name="用户",null=False,blank=False)
    order = models.ForeignKey(Order, on_delete=False,verbose_name="订单",null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=False,null=False,blank=False,verbose_name="购物车产品")
    prod_num = models.IntegerField(default=1,verbose_name="已选商品数量")
    create_date = models.DateTimeField(default=datetime.datetime.now)
    is_delete = models.BooleanField(default=False,verbose_name="已删除")
    class Meta:
        db_table="tbl_cart"
        verbose_name_plural="购物车表"

'''
产品收藏表
prod_collect
id
product
user
create_date
'''
class Prod_collect(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=False,verbose_name="收藏的商品")
    user = models.ForeignKey(User,on_delete=False,verbose_name="用户")
    create_date = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = "tbl_prod_collect"
        verbose_name_plural = "产品收藏表"

'''

评论表：
comment:
id
product 产品
user -- 评论用户
create_date -- 评论时间
content -- 评论内容
'''

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=False,verbose_name="评论商品")
    user = models.ForeignKey(User,on_delete=False,verbose_name="评论用户")
    create_date = models.DateTimeField(default=datetime.datetime.now,verbose_name="评论时间")
    content = models.TextField(max_length=200,null=False,blank=False,verbose_name="评论内容")
    class Meta:
        db_table="tbl_comment"
        verbose_name_plural = "商品评论表"









