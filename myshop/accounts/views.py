from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from shop.models import Product
from accounts.models import User
from .forms import UserRegisterForm


class LoginUser(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_message = "You Logged in successfully"
    redirect_authenticated_user = True


class LogoutUser(SuccessMessageMixin, auth_views.LogoutView):
    redirect_authenticated_user = True


class RegisterUser(SuccessMessageMixin, CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = UserRegisterForm


from django.contrib.auth.decorators import login_required


@login_required
def wishlist(request):
    # products = Product.objects.filter(users_wishlist=request.user)
    current_user = request.user
    products = current_user.wishlist.all()
    return render(request, 'accounts/user_wish_list.html', {'wishlist': products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    current_user = request.user
    if not current_user.wishlist.filter(id=id).exists():
        current_user.wishlist.add(product)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def remove_wishlist_product(request, _id):
    product = get_object_or_404(Product, id=_id)
    current_user = request.user
    if current_user.wishlist.filter(id=_id).exists():
        current_user.wishlist.remove(product)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
