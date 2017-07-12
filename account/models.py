from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from Sparrow import settings as sparrow_settings
from .mail import UserenaConfirmationMail
from .utils import get_protocol
from .managers import SparrowManager


# 用户
class User(AbstractUser):
    id = models.CharField(max_length=20, primary_key=True)
    user_avatar = models.URLField(default='https://avatars3.githubusercontent.com/u/5500125?v=3&s=460')  # 用户头像
    last_active = models.DateTimeField('last active', blank=True, null=True, help_text='The last date that the user was active.')
    activation_key = models.CharField('activation key', max_length=40, blank=True)
    signature = models.CharField('signature', max_length=100, blank=True, default='')

    objects = SparrowManager()

    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return '%s' % self.username

    def send_activation_email(self):
        """
        Sends a activation email to the user.

        This email is send when the user wants to activate their newly created
        user.

        """
        context = {'user': self,
                   'protocol': get_protocol(),
                   'activation_days': sparrow_settings.USERENA_ACTIVATION_DAYS,
                   'activation_key': self.activation_key,
                   'site': Site.objects.get_current()}

        mailer = UserenaConfirmationMail(context=context)
        mailer.generate_mail("activation")
        mailer.send_mail(self.email)

def user_can_authenticate(user):
    """
    Reject users with is_active=False. Custom user models that don't have
    that attribute are allowed.
    """
    is_active = getattr(user, 'is_active', None)
    return is_active or is_active is None


def authenticated(request, **kwargs):
    email, password = request.POST['email'], request.POST['password']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as e:
        return None
    else:
        if user.check_password(password) and user_can_authenticate(user):
            return user
    return None