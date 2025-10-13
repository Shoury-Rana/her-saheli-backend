from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import CustomUserManager

class User(AbstractUser):
    # Validator for username to allow only letters, numbers, and underscores
    username_validator = RegexValidator(
        r'^[a-zA-Z0-9_]+$',
        'Enter a valid username. This value may contain only letters, numbers, and _ characters.'
    )

    # Use a CharField for a human-readable, unique username
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and _ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    
    email = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    class HealthMode(models.TextChoices):
        MENSTRUAL = 'MENSTRUAL', 'Menstrual'
        TTC = 'TTC', 'Trying to Conceive'
        PREGNANCY = 'PREGNANCY', 'Pregnancy'
        POSTPARTUM = 'POSTPARTUM', 'Postpartum'
        MENOPAUSE = 'MENOPAUSE', 'Menopause'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_mode = models.CharField(
        max_length=20,
        choices=HealthMode.choices,
        default=HealthMode.MENSTRUAL
    )

    def __str__(self):
        return f"Profile for {self.user.username}"