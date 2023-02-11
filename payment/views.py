import stripe
from django.conf import settings
from django.db.models import Sum
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Item, Order
from django.db import IntegrityError

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(TemplateView):
	"""Шаблон для начальной страницы"""
	template_name = 'payment/home.html'

	def get_context_data(self, **kwargs):
		"""Функция для получения всех товаров из бд"""
		items = Item.objects.all()
		context = super(HomeView, self).get_context_data(**kwargs)
		context.update({
			'items': items,
			"STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
		})
		return context


class ItemView(TemplateView):
	"""Предпросмотр товара с его описанием и ценой"""
	template_name = 'payment/item.html'

	def get_context_data(self, **kwargs):
		item_id = self.kwargs['pk']
		item = Item.objects.get(id=item_id)
		context = super(ItemView, self).get_context_data(**kwargs)
		context.update({
			'item': item,
			"STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
		})
		return context


class SuccessView(TemplateView):
	"""Шаблон для отображения при удачной оплате"""
	template_name = 'payment/success.html'


class CancelView(TemplateView):
	"""Шаблон для отображения отмены оплаты"""
	template_name = 'payment/cancel.html'


class CreateCheckoutSessionView(View):
	"""Функция для получение checkout session для одного товара
	Реализовано с помощью Stripe API на основе GET запроса 'buy/<pk>' """
	def get(self, requests, *args, **kwargs):
		item_id = self.kwargs['pk']
		item = Item.objects.get(id=item_id)
		DOMAIN = 'https://django4-stripe-payment-production.up.railway.app'
		checkout_session = stripe.checkout.Session.create(
			line_items=[
				{
					'price_data': {
						'currency': 'usd',
						'unit_amount': item.price,
						'product_data': {
							'name': item.name,
						},
					},
					'quantity': 1,
				},
			],
			mode='payment',
			success_url=DOMAIN + '/success/',
			cancel_url=DOMAIN + '/cancel/',
		)
		return redirect(checkout_session.url, code=303)


class AddItemInOrderView(View):
	"""Добавление товара в заказ"""
	def get(self, requests, *args, **kwargs):
		item_id = self.kwargs['pk']
		item = Item.objects.get(id=item_id)
		new_item = Order(item_id=item.id, item_price=item.price, item_name=item.name)
		try:
			new_item.save()
			return redirect('order')
		except IntegrityError:
			return redirect('order')


class DeleteItemFromOrder(View):
	"""Удаление товара из заказа"""
	def get(self, requests, *args, **kwargs):
		item_id = self.kwargs['pk']
		item = Order.objects.get(id=item_id)
		item.delete()
		return redirect('order')


class OrderView(TemplateView):
	"""Отображение заказа в виде корзины"""
	template_name = 'payment/order.html'

	def get_context_data(self, **kwargs):
		"""Получение всех товаров из таблицы order"""
		items = Order.objects.all()
		full_price = Order.objects.aggregate(Sum('item_price'))
		count = items.count()
		full_price = full_price['item_price__sum']
		if full_price is not None:
			full_price = "{0:.2f}".format(full_price / 100)
		context = super(OrderView, self).get_context_data(**kwargs)
		context.update({
			'items': items,
			'full_price': full_price,
			'count': count,
			"STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
		})
		return context


class CreateOrderCheckoutSessionView(View):
	"""Функция для получение checkout session для заказа
	Отображение всех товаров их и общей стоимости
	Реализовано с помощью Stripe API на основе GET запроса 'buy/<pk>' """
	def get(self, requests, *args, **kwargs):
		items = Order.objects.all()
		line_items = []
		for item in items:
			line_items.append({
				'price_data': {
					'currency': 'usd',
					'unit_amount': item.item_price,
					'product_data': {
						'name': item.item_name,
					},
				},
				'quantity': 1
			})
		DOMAIN = 'http://127.0.0.1:8000'
		checkout_session = stripe.checkout.Session.create(
			line_items=line_items,
			mode='payment',
			success_url=DOMAIN + '/success/',
			cancel_url=DOMAIN + '/cancel/',
		)
		return redirect(checkout_session.url, code=303)
