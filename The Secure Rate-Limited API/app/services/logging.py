from sqlalchemy.orm import Session
from app.models.log import Log
from app.models.user import User

def add_log(db: Session, user: User, action: str, task_id: int | None = None):
    db.add(Log(user_id=user.id, task_id=task_id, action=action))
    db.commit()
