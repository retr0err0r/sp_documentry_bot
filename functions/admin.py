from models import User, get_session
from utils.logger import add_log


def process_new_admin(message, bot):
    try:
        chat_id, username = str(message.from_user.id), message.from_user.username
        session = get_session()
        user = session.query(User).filter_by(tg_id=chat_id).first()
        if not user:
            new_user = User(tg_id=chat_id, username=username, role="admin")
            session.add(new_user)
        elif user.role != "admin":
            user.role = "admin"
        session.commit()
        bot.send_message(message.chat.id, "You are Admin now!✅")
    except Exception as e:
        add_log(f"Exception in process_new_admin: {e}")

def process_ping(message, bot):
    bot.send_message(message.chat.id, "Ping!")
