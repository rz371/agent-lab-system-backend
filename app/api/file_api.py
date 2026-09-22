import os
import shutil
import time
import uuid

from pathlib import Path
from fastapi import APIRouter, File, UploadFile


from app.common.exceptions import BusinessException
from app.common.response import Response
from app.config import ALLOW_OPYIONS, MAX_FILE_SIZE, UPLOAD_DIR
from app.schemas.upload_shcemas import fileUploadResponse

router = APIRouter(prefix="/files", tags=["文件管理"])


@router.post("/upload")
def upload_files(file: UploadFile = File(...)):
    """文件上传接口"""

    # 判断有无名称
    if not file.filename:
        raise BusinessException(message="文件名不能为空")

    # 取原始的文件名 用户头像.jpg
    orignal_name = os.path.basename(file.filename)

    # 取后缀名 并转为小写
    ext = Path(orignal_name).suffix.lower()

    if ext not in ALLOW_OPYIONS:
        raise BusinessException(message=f"不支持的文件后缀：{ext}")

    # 校验文件大小
    if file.size and file.size > MAX_FILE_SIZE:
        raise BusinessException(message=f"文件不可超过:{MAX_FILE_SIZE}MB")

    # 没问题了，要存储到磁盘了
    # 存储的名称要随机性，如果一样的话，会覆盖掉
    # time.time拿到秒，变为毫秒
    disk_name = f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}{ext}"

    # 存储刚才的文件里面 -- 流式存储
    save_path = UPLOAD_DIR / disk_name  # 文件实际存储的路径
    with open(save_path, "wb") as f:
        # 从file.file读，然后逐步的写到f里面
        shutil.copyfileobj(file.file, f)

    return Response.success(
        data=fileUploadResponse(
            original_name=orignal_name,
            disk_name=disk_name,
            size=file.size,
            url=f"/uploads/{disk_name}",  # 通过服务器的IP端口加上这个静态路径就可以直接读取,前提是得在main里面声明静态目录
        )
    )
