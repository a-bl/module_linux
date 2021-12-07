from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from shop.models import Product
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
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'accounts/user_wish_list.html', {'wishlist': products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.name + ' has been removed from your Wishlist')
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, 'Added ' + product.name + ' to your Wishlist')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
