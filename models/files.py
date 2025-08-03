from sqlalchemy import ForeignKey, Integer, Text, TIMESTAMP, BigInteger, Column, String
from datetime import datetime
from zoneinfo import ZoneInfo
from base import Base


class File(Base):
    __tablename__ = "uploaded_files"

    id = Column(primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))

    url_link = Column(Text)
    file_type = Column(String(3))
    description = Column(Text)

    telegram_msg_id = Column(BigInteger, nullable=True)
    telegram_chat_id = Column(BigInteger, nullable=True)
