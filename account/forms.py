from django import forms
from django.core.exceptions import ValidationError
from .models import User
from Sparrow.settings import ALLOWED_SIGNUP_DOMAINS


# 限制用户注册邮箱的domain
def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain.')
        except Exception:
            raise ValidationError('Invalid domain.')


def UniqueEmailValidator(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('User with this Email already exists.')


# 限制用户名字
def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a forbidder word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username')


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('User with this Username already exists.')


# 表单来实现验证注册信息
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        # 排除
        exclude = ['last_login', 'last_name', 'date_joined', 'first_name']
        fields = ['username', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(SignupDomainValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)

    # 清除表单中的数据
    def clean(self):
        super(SignUpForm, self).clean()