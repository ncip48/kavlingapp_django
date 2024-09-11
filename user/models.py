from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    class UserRole(models.IntegerChoices):
        ADMIN = 0, "Admin"
        MARKETING = 1, "Marketing"
        CUSTOMER = 2, "Customer"
    
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    role = models.IntegerField(
        choices=UserRole.choices, 
        default=UserRole.ADMIN
    )
    phone = models.CharField(max_length=15)
    
    @property
    def name(self):
        # due date is calcualted 10 days from start_date
        return self.first_name + ' ' + self.last_name
    
    @property
    def role_real(self):
        if self.role == User.UserRole.ADMIN:
            return "Admin"
        elif self.role == User.UserRole.MARKETING:
            return "Marketing"
        
    @property
    def get_color(self):
        if self.role == User.UserRole.ADMIN:
            return "danger"
        elif self.role == User.UserRole.MARKETING:
            return "primary"