from sqlalchemy import Column, Integer, ForeignKey, Text, Numeric, DateTime, String, func
from models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # "debit" = هزینه، "credit" = پرداخت
    amount = Column(Numeric, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Payment(type={self.type}, amount={self.amount}, user={self.user_id})>"
