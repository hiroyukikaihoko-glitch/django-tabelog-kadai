from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')  # カートが空の場合はリダイレクト
        self.queryset = []
        self.total = 0
        for item_pk, quantity in cart["items"].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE+1)) 
        cart["total"] = self.total
        cart["tax_included_total"] = self.tax_included_total

        # 【追記】決済ビューが直接 session['total'] や session['cart'] を参照できるようにする
        self.request.session['cart'] = cart
        self.request.session['total'] = self.tax_included_total # もし税込み合計を決済で使う場合
        self.request.session.modified = True # セッションの変更をDjangoに強制保存させる

        return super().get_queryset() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["total"] = self.total
            context["tax_included_total"] = self.tax_included_total
        except Exception:
            pass
        return context

class AddCartView(LoginRequiredMixin, View):
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', None)   
        if cart is None or len(cart) == 0:
            item = OrderedDict() 
            cart = {"items": {}}
        if item_pk in cart["items"]:
            cart["items"][item_pk] += quantity
        else:
            cart["items"][item_pk] = quantity
        request.session['cart'] = cart
        return redirect('cart')

@login_required
def remove_from_cart(request, pk):  # 💡 引数を「item_pk」から「pk」に変更
    item_pk = pk                    # 💡 URLから届いた「pk」を、これまでの「item_pk」に代入
    cart = request.session.get('cart', None) 
    if cart is not None:
        del cart["items"][item_pk]
        request.session['cart'] = cart
    return redirect('/cart/')
