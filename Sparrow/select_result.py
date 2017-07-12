import random, string
from .settings import QIUNIU_ACCESS_KEY, QIUNIU_SECRET_KEY, QIUNIU_BUCKET_NAME
import qiniu


def getRandomID():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))


# 上传，可以指定过期时间
def upload_qiniu(file_path, key):
    # 生成上传凭证
    auth = qiniu.Auth(QIUNIU_ACCESS_KEY, QIUNIU_SECRET_KEY)
    upToken = auth.upload_token(QIUNIU_BUCKET_NAME, key=key)

    # 上传文件
    data, info = qiniu.put_file(upToken, key=key, file_path=file_path, mime_type="image/jpeg", check_crc=True)

    # 验证上传是否错误
    if data['key'] != key or data['hash'] != qiniu.etag(file_path):
        print('上传{0}失败'.format(key))
        return False
    else:
        print('上传{0}成功'.format(key))
        return True
