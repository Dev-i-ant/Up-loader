# src/services/queue.py
import time
from datetime import datetime, timezone
from loguru import logger
from db import SessionLocal
from models.job import UploadJob, JobStatus
from models.account import Account
from models.video import VideoAsset
from services.uploader import get_uploader
from services.uploader.base import UploadRequest

def enqueue_upload(...):
    ...

def run_worker(worker_id: int = 1):
    uploader = get_uploader()
    while True:
        with SessionLocal() as s:
            job = (s.query(UploadJob)
                    .filter(UploadJob.status == JobStatus.queued,
                            UploadJob.publish_at <= datetime.now(timezone.utc))
                    .order_by(UploadJob.created_at.asc())
                    .first())
            if not job:
                time.sleep(2); continue
            job.status = JobStatus.running; s.commit()
            acc: Account = s.get(Account, job.account_id)
            asset: VideoAsset = s.get(VideoAsset, job.asset_id)
        req = UploadRequest(file=asset.pathlike(),
                            title=job.title,
                            tags=job.tags,
                            target_type=acc.target_type,
                            target_id=acc.target_id,
                            token=acc.vk_token)
        result = uploader.upload(req)
        with SessionLocal() as s:
            job = s.get(UploadJob, job.id)
            if result.ok:
                job.status = JobStatus.done
                job.external_id = result.external_id
            else:
                job.status = JobStatus.failed
                job.error = result.error
            s.commit()
        logger.info(f"job {job.id} -> {job.status}")