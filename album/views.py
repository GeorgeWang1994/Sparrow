from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from .models import Album, Photo
from tag.models import Tag
from home.models import EventType, toAddEvent, toDelEvent, toEditEvent
from comment.models import Comment
from follow.models import Follow
from like.models import Like
from Sparrow.select_result import upload_qiniu, getRandomID
from Sparrow.settings import MEDIA_ROOT
from PIL import ImageFile
import logging, json


@login_required()
def upload(request):
    csrf_token = get_token(request)
    return render(request, 'album/create_album.html', locals())


def index(request, id):
    try:
        album = get_object_or_404(Album, id=id)
        comments = Comment.objects.filter(object_id=id).order_by('-time')
        if request.user.is_authenticated:
            follow = Follow.objects.filter(followee=album.author, follower=request.user).exists()
            is_like = Like.objects.filter(liker=request.user, liking_id=album.id).exists()
        else:
            follow = False
            is_like = False

        return render(request, 'album/index.html', locals())
    except Exception as e:
        logging.error(e)


def photo(request, id):
    try:
        photo = get_object_or_404(Photo, id=id)
        return render(request, 'album/index.html', locals())
    except Exception as e:
        logging.error(e)
        return render(request, 'album/index.html')


@login_required()
def editAlbum(request, id):
    if request.method == 'GET':
        try:
            album = get_object_or_404(Album, id=id)
            return render(request, 'album/edit_album.html', locals())
        except Exception as e:
            logging.error(e)
            return render(request, 'album/index.html', locals())
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            album = Album.objects.get(pk=id)

            tags, photos, album_desc, album_title = data["tags"], data["photos"], \
                                                    data["album_desc"], data["album_title"]
            album.tags.clear()
            for t in tags:
                tag, created = Tag.objects.get_or_create(name=t, defaults={'id':getRandomID()})
                album.tags.add(tag)

            album.photos.clear()
            for p in photos:
                photo, created = Photo.objects.get_or_create(id=p["id"], defaults={'desc': p["desc"],'url': p["url"], 'photos': album})
                album.photos.add(photo)

            album.content = album_desc
            album.title = album_title

            album.save()

            toEditEvent(id, content=album.content, title=album.title, tags=album.tags.all(), photos=album.photos.all())

            mydict = {'status': "106000"}
            return HttpResponse(json.dumps(mydict), content_type="application/json")
        except Exception as e:
            logging.error(e)
            mydict = {'status': "006000"}
            return HttpResponse(json.dumps(mydict), content_type="application/json")


@login_required()
def uploadPhoto(request):
    if request.method == 'POST':
        file = request.FILES["uploader_input"]
        parser = ImageFile.Parser()
        for chunk in file.chunks():
            parser.feed(chunk)
        img = parser.close()
        photo_id = getRandomID()
        filename = photo_id+'.jpg'
        file_path = MEDIA_ROOT + '/photo/' + filename

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(file_path)

        res = upload_qiniu(file_path, filename)
        if not res:
            logging.error('上传失败')
            data = {"id": photo_id, "status": "007003", "key": filename}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {"id": photo_id, "status": "107000", "key": filename}
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def delPhoto(request, id):
    try:
        Photo.objects.filter(pk=id).delete()
        data = {'status': '107002'}  # 成功删除
    except Exception as e:
        logging.error(e)
        data = {'status': '007004'}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def uploadAlbum(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode("utf-8"))
                album = Album.objects.create(id=getRandomID(), author=request.user)
                tags, photos, album_desc, album_title = data["tags"], data["photos"], data["album_desc"], data["album_title"]

                for t in tags:
                    tag_query = Tag.objects.filter(name=t)
                    if tag_query.count():
                        tag = Tag.objects.get(name=t)
                    else:
                        tag = Tag.objects.create(id=getRandomID(), name=t)
                    album.tags.add(tag)

                for p in photos:
                    photo = Photo.objects.create(id=p["id"], desc=p["desc"], url=p["url"], photos=album)
                    photo.save()

                album.content = album_desc
                album.title = album_title

                album.save()

                toAddEvent(EventType.ALBUM, album)

                mydict = {'status': "106000"}
                return HttpResponse(json.dumps(mydict), content_type="application/json")
            except Exception as e:
                logging.error(e)
                mydict = {'status': "006000"}
                return HttpResponse(json.dumps(mydict), content_type="application/json")


@login_required()
def delAlbum(request, id):
    Album.objects.filter(pk=id).delete()
    toDelEvent(id)
    # 从七牛中删除
    data = {'status': '0'}
    return HttpResponse(json.dumps(data), content_type="application/json")
