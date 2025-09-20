# src/services/uploader/vk_api.py
import httpx
from .base import IUploader, UploadRequest, UploadResult

class VkApiUploader(IUploader):
    def upload(self, req: UploadRequest) -> UploadResult:
        # упрощённо: псевдо-путь загрузки файла и публикации
        try:
            # 1) получить upload_url (этап зависит от конкретного эндпоинта для клипов)
            # 2) POST файл на upload_url (multipart)
            # 3) сохранить/опубликовать с метаданными (title, tags)
            # !!! Здесь заглушка. Реальные эндпоинты и поля подключим, когда подтвердим.
            return UploadResult(ok=True, external_id="stub-123")
        except Exception as e:
            return UploadResult(ok=False, error=str(e))

def get_default():
    return VkApiUploader()