from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, UserForm
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
import datetime




#------------------------------------------------------------------------------
@login_required
def profile(request):
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
            context = {'profile': profile,'user_form': user_form,'profile_form': profile_form }
            return render(request, 'page-user.html', context)
  else:
      user_form = UserForm(instance=request.user)
      profile_form = ProfileForm(instance=request.user.profile)

  context = {
  'profile': profile,
  'user_form': user_form,
  'profile_form': profile_form,
  }
  return render(request, 'page-user.html', context)





#------------------------------------------------------------------------------
@login_required
def search(request):
    if request.method=="POST":
        search = request.POST['q']
        if search:
            mold = models.Mold.objects.filter(Q(Name__icontains=search) | Q(Description__icontains=search))
            product = models.Product.objects.filter(Q(Name__icontains=search))
            manufacturer = models.Manufacturer.objects.filter(Q(Name__icontains=search) | Q(Description__icontains=search))
            repair_req = models.Repair_request.objects.filter(Q(Mold__Name__icontains=search) | Q(Description__icontains=search))
            manufacture_req = models.Manufacture_request.objects.filter(Q(Mold__Name__icontains=search) | Q(Description__icontains=search))
            component_req = models.Component_request.objects.filter(Q(Description__icontains=search))
            match = chain(mold, product, manufacturer, repair_req, manufacture_req, component_req)
            if match:
                return render(request,'search.html', {'sr': match})
            else:
                messages.error(request,  '   چیزی یافت نشد ، لطفا مجددا جستجو کنید ' )
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html', {})





#------------------------------------------------------------------------------
@login_required()
def product(request):
    products = models.Product.objects.all()
    return render(request, 'products.html', {'products': products})


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
    molds = models.Mold.objects.all()
    molds_img = models.MoldImage.objects.all()
    context = {'category':category, 'molds':molds, 'molds_img':molds_img}
    return render(request, 'category_detail.html', context)







#------------------------------------------------------------------------------
@login_required()
def buyers(request):
    buyers = models.Buyers.objects.all()
    return render(request, 'buyers.html', {'buyers': buyers})


@login_required()
def buyer_detail(request, id):
    buyer = get_object_or_404(models.Buyers, id=id)
    products = models.Product.objects.all()
    context = {'manufacturer':manufacturer, 'molds':molds, 'molds_img':molds_img}
    return render(request, 'buyer_detail.html', context)








#------------------------------------------------------------------------------
@login_required()
def manufacture_req(request):
    reject_req = models.Manufacture_request.objects.filter(Status='رد شده').count()
    total_req = models.Manufacture_request.objects.all().count()
    done_req = models.Manufacture_request.objects.filter(Status='به اتمام رسیده').count()
    manufacture_requests = models.Manufacture_request.objects.all().order_by("-StartTime")
    return render(request, 'manufacture_req.html', {'manufacture_requests': manufacture_requests,
    'reject_req':reject_req,
    'total_req':total_req,
    'done_req':done_req
    })


@login_required()
def manufacture_req_detail(request, id):
    manufacture_request = get_object_or_404(models.Manufacture_request, id=id)
    context = {'manufacture_request':manufacture_request}
    return render(request, 'manufacture_req_detail.html', context)











# End
