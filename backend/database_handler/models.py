from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    # To create simple user, use the following command:
    # python manage.py createuser
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        
        # hash the password
        user.set_password(password)
        user.save()
        
        return user
    
    # python manage.py createsuperuser
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def get_full_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    
    
class PatientImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(null=False, upload_to='images/')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    classification = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.user.name + ' ' + str(self.image)
    
    def getImage(self):
        return f'http://localhost:8000{self.image.url}' if self.image else ''
    
    class Meta:
        ordering = ['image_id']
