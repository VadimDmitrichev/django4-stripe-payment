from django.db import models


class Item(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	price = models.IntegerField(default=1) # центы

	def __str__(self):
		return self.name

	def get_display_price(self):
		"""Функция для преобразования цены из центов в доллары"""
		return "{0:.2f}".format(self.price / 100)


class Order(models.Model):
	"""Модель для сохранения товаров в заказ"""
	item_id = models.IntegerField(unique=True)
	item_name = models.CharField(max_length=100)
	item_price = models.IntegerField()

	def __str__(self):
		return self.item_name

	def get_display_price(self):
		return "{0:.2f}".format(self.item_price / 100)
