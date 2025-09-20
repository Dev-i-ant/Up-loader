# src/services/uploader/base.py
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Optional

@dataclass
class UploadRequest:
    file: Path
    title: str
    tags: list[str]
    target_type: str  # "group" | "profile"
    target_id: int
    token: str

@dataclass
class UploadResult:
    ok: bool
    external_id: Optional[str] = None
    error: Optional[str] = None

class IUploader(Protocol):
    def upload(self, req: UploadRequest) -> UploadResult: ...