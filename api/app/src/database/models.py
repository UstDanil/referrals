from uuid import uuid4
from sqlalchemy import MetaData, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData())


class User(Base):
    __tablename__ = 'users'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    referrer_id = Column(postgresql.UUID(as_uuid=True), nullable=True)

    referral_codes = relationship('ReferralCode', cascade="all, delete", lazy='subquery')


class ReferralCode(Base):
    __tablename__ = 'referrer_codes'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    code = Column(String(), nullable=False)
    end_date = Column(DateTime(), nullable=False)

    user = relationship(User, back_populates='referral_codes')
