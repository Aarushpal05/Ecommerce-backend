from django.db import models
from django.contrib.auth.models import User

class category(models.Model):
    name= models.CharField(max_length=255)
    pic= models.ImageField(upload_to='media/category/', blank=True, null=True )

    def __str__(self):
        return self.name

class AddProduct(models.Model):
    category= models.ForeignKey(category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    pic = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('AddProduct', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class Order(models.Model):
        PAYMENT_CHOICES = (
            ('COD', 'Cash On Delivery'),
            ('ONLINE', 'Online Payment'),
        )

        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        full_name = models.CharField(max_length=200)
        email = models.EmailField()
        phone = models.CharField(max_length=15)
        address = models.TextField()

        payment_method = models.CharField(
            max_length=10,  
            choices=PAYMENT_CHOICES     
        )
    
        total_price = models.DecimalField(max_digits=10, decimal_places=2)

        payment_link = models.URLField(blank=True, null=True)

        created_at = models.DateTimeField(auto_now_add=True)
    
        def __str__(self):  
            return self.user.username if self.user else self.full_name

# # class OrderItem(models.Model):
# #         order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
# #         product_name = models.CharField(max_length=255)
# #         quantity   = models.IntegerField()
# #         price = models.DecimalField(max_digits=10, decimal_places=2)
       

# #          @property
# #     def total_price(self):
# #         return self.quantity * self.price

    

# #         def __str__(self):
# #             return self.product_name    
# # 
# # 
# # class Order(models.Model):
#     customer_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.customer_name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product_name    
