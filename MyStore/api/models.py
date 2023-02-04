from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
class Products(models.Model):

    name=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    image=models.ImageField(null=True,upload_to="images")

    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if  ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0
    @property
    def no_reviews(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0


    def __str__(self):
        return self.name

class Carts(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
            ("order-placed","order-placed"),
            ("in-cart","in-cart"),
            ("cancelled","cancelled")

    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")


class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.comment


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
            ("order-placed","order-placed"),
            ("dispatched","dispatched"),
            ("in-transit","in-transit"),
            ("cancelled","cancelled")

    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=250)
    phone=models.CharField(max_length=20)



#products.objects.create(name="samsung",price=30000,description="RAM-8",category="mobile",image=)
#rs=Products.objects.all()
#rs
#rs=Products.objects.filter(category="mobile")
#rs=Products.objects.all().exclude(category='mobile')
#update
#Products.objects.filter(id=2).update(price=500)






