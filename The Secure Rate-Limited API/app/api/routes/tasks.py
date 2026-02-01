from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.task import TaskCreate, TaskOut
from app.models.tasks import Task
from app.models.user import User
from app.core.rate_limit import check_rate_limit
from app.services.logging import add_log

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut)
def create_task(
    payload: TaskCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # per-user rate limit
    check_rate_limit(f"user:{user.id}")

    task = Task(title=payload.title, description=payload.description, owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)

    add_log(db, user, "CREATE_TASK", task_id=task.id)
    return task

@router.get("", response_model=list[TaskOut])
def list_tasks(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    check_rate_limit(f"user:{user.id}")
    return db.query(Task).filter(Task.owner_id == user.id).order_by(Task.id.desc()).all()
