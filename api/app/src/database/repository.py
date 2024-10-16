from uuid import uuid4
from sqlalchemy import select, update, delete

from src.database.models import User, ReferralCode


class Repository:
    def __init__(self, session):
        self.session = session
        self.model_user = User
        self.model_referrer_code = ReferralCode

    async def create_user(self, name, email, password, referrer_id):
        new_user = self.model_user(
            id=uuid4(),
            name=name,
            email=email,
            password=password,
            referrer_id=referrer_id
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user.id

    async def get_user_by_email(self, email):
        query = select(self.model_user).where(self.model_user.email == email)
        result = await self.session.execute(query)
        return result.scalar()

    async def delete_referrer_code_by_user_id(self, user_id):
        query = delete(self.model_referrer_code).where(self.model_referrer_code.user_id == user_id)
        await self.session.execute(query)
        await self.session.commit()

    async def get_referrer_code_by_user_id(self, user_id):
        query = select(self.model_referrer_code).where(self.model_referrer_code.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_referrer_by_referrer_code(self, referrer_code):
        query = select(self.model_referrer_code).where(self.model_referrer_code.code == referrer_code)
        result = await self.session.execute(query)
        return result.scalar()

    async def create_referrer_code(self, user_id, referrer_code, code_end_date):
        new_code = self.model_referrer_code(
            id=uuid4(),
            user_id=user_id,
            code=referrer_code,
            end_date=code_end_date
        )
        self.session.add(new_code)
        await self.session.commit()

    async def get_user_referrals_by_user_id(self, user_id):
        query = select(self.model_user).where(self.model_user.referrer_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
