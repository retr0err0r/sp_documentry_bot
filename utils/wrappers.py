from models import get_session, User
from utils.logger import add_log


def check_username():
    def decorator(handler):
        def wrapper(message):
            try:
                chat_id, username = str(message.from_user.id), message.from_user.username
                with get_session() as session:
                    user = session.query(User).filter_by(tg_id=chat_id).first()
                    if not user:
                        new_user = User(tg_id=chat_id, username=username)
                        session.add(new_user)
                    elif user.username != username:
                        user.username = username
                    session.commit()
                return handler(message)
            except Exception as e:
                add_log(f"Exception in check_username: {e}")

        return wrapper

    return decorator


def check_admin(bot):
    def decorator(handler):
        def wrapper(message):
            try:
                chat_id = str(message.from_user.id)
                with get_session() as session:
                    user = session.query(User).filter_by(tg_id=chat_id).first()
                if user and user.role == "admin":
                    return handler(message)
                text = "You must log in to the bot first ⛔️\nAsk the admin to add you."
                if user:
                    text = "You are not admin, and you can't access this command ⛔️"
                bot.send_message(chat_id, text)
            except Exception as e:
                add_log(f"Exception in check_admin: {e}")

        return wrapper

    return decorator
