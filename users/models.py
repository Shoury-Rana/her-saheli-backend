from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    class HealthMode(models.TextChoices):
        MENSTRUAL = 'menstrual', 'Menstrual'
        TTC = 'ttc', 'Trying to Conceive'
        PREGNANCY = 'pregnancy', 'Pregnancy'
        POSTPARTUM = 'postpartum', 'Postpartum'
        MENOPAUSE = 'menopause', 'Menopause'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    average_cycle = models.PositiveSmallIntegerField(default=28)
    
    selected_mode = models.CharField(
        max_length=20,
        choices=HealthMode.choices,
        default=HealthMode.MENSTRUAL
    )
    menstrual_mode = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"
    
    def save(self, *args, **kwargs):
        # Automatically set menstrual_mode based on selected_mode
        self.menstrual_mode = (self.selected_mode == self.HealthMode.MENSTRUAL)
        super().save(*args, **kwargs)