from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user_model
from django.utils.six import text_type
from django.utils.encoding import smart_text
from .utils import generate_sha1
from Sparrow.select_result import getRandomID
import re

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class SparrowManager(UserManager):
    """ Extra functionality for the Userena model. """

    def createuser(self, username, email, password, active=False, send_email=True):
        """
        A simple wrapper that creates a new :class:`User`.

        :param username:
            String containing the username of the new user.

        :param email:
            String containing the email address of the new user.

        :param password:
            String containing the password for the new user.

        :param active:
            Boolean that defines if the user requires activation by clicking
            on a link in an e-mail. Defaults to ``False``.

        :param send_email:
            Boolean that defines if the user should be sent an email. You could
            set this to ``False`` when you want to create a user in your own
            code, but don't want the user to activate through email.

        :return: :class:`User` instance representing the new user.

        """

        new_user = get_user_model().objects.create_user(
            username=username, email=email, password=password, is_active=active, id=getRandomID())

        userena_profile = self.create_userena_profile(new_user)
        if send_email:
            userena_profile.send_activation_email()

        return new_user

    # 设置activation_key
    def create_userena_profile(self, user):
        """
        Creates an :class:`UserenaSignup` instance for this user.

        :param user:
            Django :class:`User` instance.

        :return: The newly created :class:`UserenaSignup` instance.

        """
        if isinstance(user.username, text_type):
            user.username = smart_text(user.username)
        salt, activation_key = generate_sha1(user.username)

        try:
            self.filter(username=user.username, email=user.email).update(activation_key=activation_key)
            profile = get_user_model().objects.get(username=user.username, email=user.email)
        except self.model.DoesNotExist:
            profile = self.create(user=user,
                                  activation_key=activation_key)
        return profile