# src/services/uploader/__init__.py
from .vk_api import get_default as get_vk
from .base import IUploader

def get_uploader(name: str = "vk_api") -> IUploader:
    if name == "vk_api":
        return get_vk()
    elif name == "headless":
        from .headless import HeadlessUploader
        return HeadlessUploader()
    raise ValueError("Unknown uploader")