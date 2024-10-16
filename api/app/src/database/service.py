from src.init_database import session_maker
from src.database.repository import Repository


async def get_user_by_email(user_email):
    async with session_maker() as session:
        repository = Repository(session)
        user = await repository.get_user_by_email(user_email)
    return user


async def create_user_in_base(user_info, referrer_id):
    async with session_maker() as session:
        repository = Repository(session)
        user_id = await repository.create_user(user_info.name, user_info.email, user_info.password, referrer_id)
    return user_id


async def get_referrer_code_by_user_id(user_id):
    async with session_maker() as session:
        repository = Repository(session)
        referrer_code = await repository.get_referrer_code_by_user_id(user_id)
    return referrer_code


async def get_referrer_by_referrer_code(referrer_code):
    async with session_maker() as session:
        repository = Repository(session)
        referrer_code = await repository.get_referrer_by_referrer_code(referrer_code)
    return referrer_code.user_id if referrer_code else None


async def create_referrer_code_in_base(user_id, referrer_code, code_end_date):
    async with session_maker() as session:
        repository = Repository(session)
        await repository.delete_referrer_code_by_user_id(user_id)
        await repository.create_referrer_code(user_id, referrer_code, code_end_date)


async def delete_referrer_code_from_base(user_id):
    async with session_maker() as session:
        repository = Repository(session)
        await repository.delete_referrer_code_by_user_id(user_id)


async def get_user_referrals_from_base(user_id):
    async with session_maker() as session:
        repository = Repository(session)
        user_referrals = await repository.get_user_referrals_by_user_id(user_id)
    return user_referrals
