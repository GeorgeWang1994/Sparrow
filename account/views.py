from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from PIL import ImageFile, Image
from .models import User, authenticated
from post.models import Post
from album.models import Album
from follow.models import Follow
from home.models import Event
from Sparrow.select_result import upload_qiniu, getRandomID
from Sparrow.settings import MEDIA_ROOT, QIUNIU_IMG_BASE_URL
import json, logging
import shutil
import os.path

logger = logging.getLogger('account.views')

# 登陆
def signin(request):
    try:
        if request.method == 'POST':
            user = authenticated(request)
            if user is None:
                return render(request, 'account/login.html')

            login(request, user)
            logging.info('login success')

            data = {'status': '104001'}  # 返回登录成功

            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
    return render(request, 'account/login.html', locals())


# 注册
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.createuser(username, email, password)

        data = {'status': '104000'}

        return HttpResponse(json.dumps(data),content_type="application/json")
    if request.method == 'GET':
        return render(request, 'account/register.html', locals())


# 退出登录
def signout(request):
    try:
        logout(request)
    except Exception as e:
        logging.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 激活邮件
def email_activate(request):
    return render(request, 'account/login.html', locals())


# 个人主页
@login_required()
def getInfo(request):
    try:
        if request.method == 'POST':
            username = request.POST["user_name"]
            desc = request.POST["user_desc"]
            User.objects.filter(pk=request.user.id).update(username=username, signature=desc)
            data = {'status': '115000'}

            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
    else:
        return render(request, 'account/setting/info.html', locals())


@login_required()
def getSecurity(request):
    try:
        if request.method == 'POST':
            old_pwd = request.POST["old_pwd"]
            new_pwd = request.POST["new_pwd"]
            request.user.check_password(new_pwd)
            data = {'status': '102003'}

            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
    else:
        return render(request, 'account/setting/security.html', locals())


# 处理个人头像信息
@login_required()
def getAvatar(request):
    return render(request, 'account/setting/avatar.html', locals())


@login_required()
def uploadAvatar(request):
    try:
        if request.method == 'POST':
            file = request.FILES["avatar_file"]
            parser = ImageFile.Parser()
            for chunk in file.chunks():
                parser.feed(chunk)
            img = parser.close()
            photo_id = getRandomID()
            filename = photo_id+'.jpg'
            file_path = MEDIA_ROOT + '/avatar/' + filename

            try:
                if os.path.isdir(MEDIA_ROOT + '/avatar/'):
                    shutil.rmtree(MEDIA_ROOT + '/avatar/')
                os.mkdir(MEDIA_ROOT + '/avatar/')
            except Exception as e:
                logging.error(e)
                return

            if img.mode != "RGB":
                img = img.convert("RGB")

            img.save(file_path)

            data = {"status": "114000", "key": filename}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        return render(request, '404.html', locals())


@login_required()
def saveavatar(request):
    # 先进行验证
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                x, y, width, height = int(request.POST["x"]), int(request.POST["y"]), int(request.POST["width"]), int(request.POST["height"])
                photo_id = request.POST["photo_id"]
                file_path = MEDIA_ROOT + '/avatar/' + photo_id
                if not os.path.isfile(file_path):
                    logging.error("this path is not file")
                    return

                user = request.user

                img = Image.open(file_path)

                if img.mode != "RGBA":
                    img = img.convert("RGBA")

                bounds = (x, y, width, height)
                img = img.crop(bounds)
                img = img.resize((220, 220),Image.ANTIALIAS)
                img.save(file_path, 'png')
                img.close()

                res = upload_qiniu(file_path, photo_id)
                if not res:
                    logging.error('上传失败')
                    data = {"status": "014001"}
                else:
                    user.user_avatar = QIUNIU_IMG_BASE_URL + photo_id
                    user.save()
                    data = {"status": "114001"}
            else:
                data = {"status": "014001"}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        return render(request, '404.html', locals())

# 个人信息
def user(request, id):
    try:
        user = User.objects.get(pk=id)
        follower_count = Follow.objects.filter(followee=user).count()  # 粉丝
        following_count = Follow.objects.filter(follower=user).count()  # 关注的人
        all_post_count = Event.objects.filter(author=user).count()  # 所有文章
        posts = Post.objects.filter(author__id=id)
        albums = Album.objects.filter(author__id=id)
        if request.user.is_authenticated:
            follow = Follow.objects.filter(followee__id=id, follower=request.user).exists()
        else:
            follow = False
        return render(request, 'user/index.html', locals())
    except Exception as e:
        logging.error(e)
        return render(request, '404.html', locals())