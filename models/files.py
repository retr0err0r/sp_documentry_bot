from sqlalchemy import ForeignKey, Integer, Text, BigInteger, Column, String
from models.base import Base


class File(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))

    url_link = Column(Text)
    file_type = Column(String(3))
    description = Column(Text)

    telegram_msg_id = Column(BigInteger, nullable=True)
    telegram_chat_id = Column(BigInteger, nullable=True)

    def __repr__(self):
        return f"<File {self.url_link}>"
