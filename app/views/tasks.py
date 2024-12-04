import json
import os
import tempfile
from pathlib import Path

from anyio import wrap_file
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app import translation
from app.deps import CurrentUser, dbDep
from app.utils.config import settings
from app.models import TaskCreate, Task, TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def create_task(task: TaskCreate, current_user: CurrentUser, db: dbDep):
    db_task = TaskCreate.model_validate(task, update={"user_id": current_user.id})
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"task_id": db_task.id}


@router.post("/{task_id}/translate")
def translate_task(task_id: int, db: dbDep):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.status != 'pending':
        raise HTTPException(status_code=400, detail="Task is already in progress or completed")

    # 调用外部 LLM API 进行翻译
    translated_content = translation.translate_content(db_task.original_content, db_task.source_language,
                                                       db_task.target_language)

    db_task.status = 'completed'
    db_task.translated_content = translated_content
    db.commit()
    db.refresh(db_task)

    return {"task_id": db_task.id, "status": db_task.status}


@router.get("/{task_id}", response_model=TaskStatus)
def get_task_status(task_id: int, db: dbDep):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": db_task.status, "translated_content": db_task.translated_content}


@router.get("/{task_id}/download")
async def download_task(task_id: int, db: dbDep):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    content = json.dumps(db_task.translated_content)
    with tempfile.NamedTemporaryFile('w',
                                     delete=False,
                                     dir=settings.DOWNLOAD_DIRECTORY) as f:
        f = wrap_file(f)
        await f.write(content)
        src = f.name
    file_path = Path(settings.DOWNLOAD_DIRECTORY / f"{task_id}.json")
    os.rename(src, file_path)
    return FileResponse(file_path)
