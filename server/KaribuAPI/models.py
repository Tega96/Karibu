from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models


# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('name',)
    
    # Type of object returned when this model is queried
    def __str__(self):
        return self.name
    
    # URL to access the object
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
# Product model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_added',)
    
    # Type of object returned when this model is queried
    def __str__(self):
        return self.name
    
    # URL to access the object
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8080' + self.image.url
        return ''
    
    # Save the image as a thumbnail
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8080' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://' + self.thumbnail.url
            else:
                return ''
            
    

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                in_mem_file = BytesIO()
                img.save(in_mem_file, 'JPEG')
                self.image = File(in_mem_file, name=f'{self.image.name}')
        super().save(*args, **kwargs)
