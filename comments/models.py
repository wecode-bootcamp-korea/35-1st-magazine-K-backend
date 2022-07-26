from django.db import models

from core.models import TimeStampModel

class Comment(TimeStampModel):
    user    = models.ForeignKey('users.user', on_delete=models.CASCADE)
    product = models.ForeignKey('products.product', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    rating  = models.DecimalField(max_digits=2, decimal_places=1, null=True)

    class Meta: 
        db_table = 'comments'
