from django.db import models
from datetime import datetime
from .resources import POSITIONS



# CREATE TABLE STAFF (
#     staff_id INT AUTO_INCREMENT NOT NULL,
#     full_name CHAR(255) NOT NULL,
#     position CHAR(255) NOT NULL,
#     labor_contract INT NOT NULL,
#
#     PRIMARY KEY (staff_id)
# );


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default='CA')
    labor_contact = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]
# CREATE TABLE PRODUCTS (
#     product_id INT AUTO_INCREMENT NOT NULL,
#     name CHAR(255) NOT NULL,
#     price FLOAT NOT NULL,
#
#     PRIMARY KEY (product_id)
# );


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


# cap = Product(name='Монитор', price=9999.0)
# cap.save()
# product_1 = Product(name='Витая пара(3м)', price=993.0)
# cap.save()
# product_2 = Product.objects.create(name='Клавиатура', price=1060.0)
# CREATE TABLE ORDERS (
#     order_id INT AUTO_INCREMENT NOT NULL,
# time_in DATETIME NOT NULL,
# time_out DATETIME,
# cost FLOAT NOT NULL,
# pickup INT NOT NULL,
# staff INT NOT NULL,
#
# PRIMARY KEY(order_id),
# FOREIGN KEY(staff) REFERENCES STAFF(staff_id)
# );


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField("Product", through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete: # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds()
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now() - self.time_in).total_seconds()

# CREATE TABLE PRODUCTS_ORDERS (
#     product_order_id INT AUTO_INCREMENT NOT NULL,
#     product INT NOT NULL,
#     in_order INT NOT NULL,
#     amount INT NOT NULL,
#
#     PRIMARY KEY (product_order_id),
#     FOREIGN KEY (product) REFERENCES PRODUCTS (product_id),
#     FOREIGN KEY (in_order) REFERENCES ORDERS (order_id)
# );


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def product_sum(self):
        return self.product.price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

