from models.base import get_session
from models.users import User


def is_admin(tg_id: str) -> bool:
    session = get_session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    return user and user.role == "admin"
