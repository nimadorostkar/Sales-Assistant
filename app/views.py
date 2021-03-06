from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from django.contrib.auth.models import User
from .models import Profile, Buyers, Product_qty, Purchase_request
from .forms import ProfileForm, UserForm
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import user_passes_test





#------------------------------------------------------------------------------
@login_required
def profile(request):
    user_requests = models.Purchase_request.objects.filter(user=request.user).order_by("-date")
    profile = models.Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            password1 = user_form.cleaned_data['password1']
            password2 = user_form.cleaned_data['password2']
            phone = profile_form.cleaned_data['phone']
            address = profile_form.cleaned_data['address']
            user_photo = profile_form.cleaned_data['user_photo']
            user_form.save()
            profile_form.save()
            context = {'profile': profile,'user_form': user_form,'profile_form': profile_form, 'user_requests':user_requests }
            return render(request, 'page-user.html', context)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
    'profile': profile,
    'user_form': user_form,
    'profile_form': profile_form,
    'user_requests':user_requests
    }
    return render(request, 'page-user.html', context)





#------------------------------------------------------------------------------
@login_required
def search(request):
    if request.method=="POST":
        search = request.POST['q']
        if search:
            product = models.Product.objects.filter(Q(name__icontains=search) | Q(code__icontains=search) | Q(description__icontains=search) )
            buyers = models.Buyers.objects.filter(Q(name__icontains=search) | Q(description__icontains=search) )
            match = chain(product, buyers)
            if match:
                return render(request,'search.html', {'sr': match})
            else:
                messages.error(request,  '   ???????? ???????? ?????? ?? ???????? ?????????? ?????????? ???????? ' )
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html', {})





#------------------------------------------------------------------------------
@login_required()
def product(request):
    products = models.Product.objects.all()
    context = {'products':products}
    return render(request, 'products.html', context)


@login_required()
def product_detail(request, id):
    product = get_object_or_404(models.Product, id=id)
    context = {'product':product}
    return render(request, 'product_detail.html', context)






#------------------------------------------------------------------------------
@login_required()
def category(request):
    category = models.Category.objects.all()
    return render(request, 'category.html', {'category': category})


@login_required()
def category_detail(request, id):
    category = get_object_or_404(models.Category, id=id)
    products = models.Product.objects.filter(category=category)
    context = {'category':category, 'products':products}
    return render(request, 'category_detail.html', context)







#------------------------------------------------------------------------------
@login_required()
def buyers(request):
    buyers = models.Buyers.objects.all()
    return render(request, 'buyers.html', {'buyers': buyers})


@login_required()
def buyer_detail(request, id):
    buyer = get_object_or_404(models.Buyers, id=id)
    buyer_requests = models.Purchase_request.objects.filter(buyer=buyer)
    context = {'buyer':buyer, 'buyer_requests':buyer_requests}
    return render(request, 'buyer_detail.html', context)







#------------------------------------------------------------------------------
#@user_passes_test(lambda u: u.is_superuser)
@login_required()
def purchase_request(request):
    new_req = models.Purchase_request.objects.filter(status='????????').count()
    total_req = models.Purchase_request.objects.all().count()
    checked_req = models.Purchase_request.objects.filter(status='???????? ??????').count()
    purchase_requests = models.Purchase_request.objects.all().order_by("-date")
    return render(request, 'purchase_request.html', {'purchase_requests': purchase_requests,
    'new_req':new_req,
    'total_req':total_req,
    'checked_req':checked_req
    })


#@user_passes_test(lambda u: u.is_superuser)
@login_required()
def purchase_request_detail(request, id):
    purchase_request = get_object_or_404(models.Purchase_request, id=id)
    product_qty = models.Product_qty.objects.filter(property=purchase_request)
    if request.method=="POST":
        obj = purchase_request
        obj.status = '???????? ??????'
        obj.save()
    #if request.method=="GET":
        #obj = purchase_request
        #obj.delete()
    return render(request, 'purchase_request_detail.html', {'purchase_request':purchase_request, 'product_qty':product_qty})





#------------------------------------------------------------------------------
@login_required()
def register_buyer(request):
    count = models.Buyers.objects.all().count()
    if request.method=="POST":
        obj = Buyers()
        obj.name = request.POST['name']
        obj.phone_number = request.POST['phone_number']
        obj.address = request.POST['address']
        obj.description = description = request.POST['description']
        obj.save()
        count = models.Buyers.objects.all().count()
        return render(request, 'register_buyer.html', {'count':count})
    else:
        return render(request, 'register_buyer.html', {'count':count})







#------------------------------------------------------------------------------
@login_required()
def register_purchase_request(request):
    products = models.Product.objects.all()
    buyers = models.Buyers.objects.all()
    if request.method=="POST":
        req = Purchase_request()
        req.user = request.user
        req.buyer = get_object_or_404(models.Buyers, id=request.POST.get('buyer'))
        req.method = request.POST['method']
        req.discount = request.POST['discount']
        req.description = request.POST['description']
        req.save()

        obj = Product_qty()
        obj.product = get_object_or_404(models.Product, id=request.POST.get('product-0'))
        obj.qty = request.POST['qty-0']
        obj.property = req
        obj.save()

        tot_counter = int(request.POST['tot-counter'])
        for x in range(tot_counter):
            obj = Product_qty()
            obj.product = get_object_or_404(models.Product, id=request.POST.get('product-'+str(x+1)))
            obj.qty = request.POST['qty-'+str(x+1)]
            obj.property = req
            obj.save()

        return render(request, 'register_purchase_request.html', {'products':products, 'buyers':buyers})
    else:
        return render(request, 'register_purchase_request.html', {'products':products, 'buyers':buyers})












# End
