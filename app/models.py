from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator



#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس  ")
  address = models.CharField(max_length=3000,null=True, blank=True,verbose_name = " آدرس  ")
  user_photo = models.ImageField(upload_to='user_uploads/user_photo',default='user_uploads/user_photo/default.png',null=True, blank=True,verbose_name = "تصویر کاربر")


  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()

  def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.user_photo.url))

  def user_name(self):
        return str(self.user)

  class Meta:
      verbose_name = "پروفایل"
      verbose_name_plural = " پروفایل ها "

  def __str__(self):
    return "پروفایل : " + str(self.user)








#------------------------------------------------------------------------------
class Buyers(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name = "نام")
    phone_number = models.CharField(max_length=50,null=True, blank=True,verbose_name = "شماره تلفن")
    address=models.CharField(max_length=200,null=True, blank=True,verbose_name = "آدرس")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name = "توضیحات")


    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('app:buyer_detail',args=[self.id])

    class Meta:
        verbose_name = "خریدار"
        verbose_name_plural = "خریداران"





#------------------------------------------------------------------------------
class Category(MPTTModel):
    name = models.CharField(max_length=200, unique=True, verbose_name = "نام")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name = "والد")


    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def get_absolute_url(self):
        return reverse('app:category_detail',args=[self.id])

    def __unicode__(self):
        return u"%s" % (self.name)

    def __str__(self):
        return str(self.name)





#------------------------------------------------------------------------------
#Unique code and name
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name = "نام")
    code = models.CharField(max_length=40, verbose_name = "کد")
    qty_in_box = models.IntegerField(verbose_name = "تعداد در کارتن")
    price = models.CharField(max_length=40, verbose_name = "قیمت ( ریال )")
    category = models.ForeignKey(Category ,on_delete=models.CASCADE ,null=True, blank=True, verbose_name = "دسته بندی")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name = "توضیحات")
    image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")



    def __str__(self):
      return str(self.name)

    @property
    def price_display(self):
        return "%s ریال " % self.price

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    def get_absolute_url(self):
        return reverse('app:product_detail',args=[self.id])

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"







#------------------------------------------------------------------------------
class Purchase_request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "کارشناس فروش")
    #product = models.ManyToManyField(Product_qty, verbose_name = "محصول و تعداد")
    buyer = models.ForeignKey(Buyers ,on_delete=models.CASCADE, verbose_name = "خریدار")
    description=models.TextField(max_length=1000, null=True, blank=True, verbose_name = "توضیحات")
    CHOICES1 = ( ('نقدی پای بار','نقدی پای بار'), ('چک یک ماهه','چک یک ماهه'), ('چک دو ماهه','چک دو ماهه'), ('چک سه ماهه','چک سه ماهه') )
    method = models.CharField(max_length=30,choices=CHOICES1, verbose_name = "روش تسویه")
    discount = models.IntegerField(default='0',validators=[MinValueValidator(0),MaxValueValidator(100)], verbose_name = "درصد تخفیف" )
    date = jmodels.jDateField(auto_now_add=True, verbose_name = "تاریخ")
    CHOICES2 = ( ('جدید','جدید'), ('برسی شده','برسی شده') )
    status= models.CharField(max_length=20,choices=CHOICES2, default='جدید', verbose_name = "وضعیت")


    def __str__(self):
        return ' شماره درخواست ' + str(self.id) + ' توسط ' + self.user.username + ' برای ' + self.buyer.name + ' در تاریخ ' + str(self.date)

    def get_absolute_url(self):
        return reverse('app:purchase_request_detail',args=[self.id])

    class Meta:
        verbose_name = "درخواست خرید"
        verbose_name_plural = "درخواست های خرید"


class Product_qty(models.Model):
    property = models.ForeignKey(Purchase_request, on_delete=models.CASCADE, related_name='request' , verbose_name = "درخواست")
    product = models.ForeignKey(Product ,on_delete=models.CASCADE, verbose_name = "محصول")
    qty = models.IntegerField(verbose_name = "تعداد" )

    def __str__(self):
        return str(self.qty) + ' عدد ' + self.product.name

    class Meta:
        verbose_name = "تعداد محصول"
        verbose_name_plural = "تعداد محصول"








# End
