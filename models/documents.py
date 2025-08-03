from sqlalchemy import ForeignKey, Integer, Text, Date, Numeric, Column, String
from sqlalchemy.orm import relationship

from models.base import Base


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(ForeignKey("users.id"))

    cotej_number = Column(Numeric)
    booking_number = Column(Numeric)
    container_quantity = Column(Integer)
    container_size = Column(String)
    goods_type = Column(Text)
    assignment_date = Column(Date)

    shipping_company = Column(Text)
    cargo_owner = Column(Text)
    production_center = Column(Text)

    document_status = Column(Text)
    payment_status = Column(Text)

    compartment_name = Column(Text)
    flexis_supplier = Column(Text)
    flexis_used_quantity = Column(Integer)

    files = relationship("File", backref="document")

    def __repr__(self):
        return (
            f"<Document(cotej_number={self.cotej_number}, booking_number={self.booking_number},\n"
            f"\tclient_id={self.client_id}),\n"
            f"\tshipping_company={self.shipping_company}, cargo_owner={self.cargo_owner})>"
        )
