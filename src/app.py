# src/app.py (фрагмент)
@app.command()
def batch_upload(account_id: int,
                 dir: Path,
                 meta: Path,
                 start_at: str = typer.Option("now"),
                 interval: str = typer.Option("15m"),
                 shuffle: bool = False):
    """
    Поставить пачку клипов из папки с метой построчно.
    """
    from services.meta import load_meta_file
    from services.queue import enqueue_batch
    assets = sorted([p for p in dir.iterdir() if p.suffix.lower() in (".mp4",".mov",".webm")])
    if shuffle:
        import random; random.shuffle(assets)

    metas = load_meta_file(meta)
    if not metas:
        raise RuntimeError("Meta file is empty or invalid")

    # выравниваем списки по минимальной длине
    n = min(len(assets), len(metas))
    assets = assets[:n]; metas = metas[:n]

    from datetime import datetime, timezone, timedelta
    def parse_interval(s: str) -> timedelta:
        # 10m, 2h, 1d
        num = int(s[:-1]); unit = s[-1]
        return {"m": timedelta(minutes=num), "h": timedelta(hours=num), "d": timedelta(days=num)}[unit]

    base_time = datetime.now(timezone.utc) if start_at == "now" else datetime.fromisoformat(start_at)
    delta = parse_interval(interval)

    from db import SessionLocal
    from models.account import Account
    from models.video import VideoAsset
    from models.job import UploadJob, JobStatus

    with SessionLocal() as s:
        acc = s.get(Account, account_id); assert acc and acc.target_type=="profile", "Нужен аккаунт профиля"
        created = []
        for i, (path, m) in enumerate(zip(assets, metas)):
            publish_at = base_time + i*delta
            asset = VideoAsset(prepared_path=str(path))
            s.add(asset); s.flush()
            job = UploadJob(
                account_id=acc.id, asset_id=asset.id,
                title=m["title"], tags=m["tags"],
                publish_at=publish_at, status=JobStatus.queued
            )
            s.add(job); created.append(job)
        s.commit()
    print(f"[green]Queued {len(created)} jobs[/] starting {base_time.isoformat()} every {interval}")