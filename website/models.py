from django.db import models

# Create your models here.
class Site(models.Model):
    id = models.AutoField(primary_key=True)
    logo = models.FileField(max_length=100, null=True)
    nama_website = models.CharField(max_length=50)
    nama_perusahaan = models.CharField(max_length=50)
    alamat = models.TextField()
    email = models.EmailField()
    template_kavling = models.TextField()
    no_telp = models.CharField(max_length=15, null=True)
    no_hp = models.CharField(max_length=15)
    placement_template = models.TextField()
    ttd = models.FileField(null=True, max_length=100)
    class Meta:
        # define table name
        db_table = 'site'
        
