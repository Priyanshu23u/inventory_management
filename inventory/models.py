from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)  # ✅ Explicit ID field
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
