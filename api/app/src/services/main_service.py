import os
import random
import string
from datetime import datetime, timedelta
from src.database.service import get_user_by_email, create_user_in_base, get_referrer_code_by_user_id, \
    get_referrer_by_referrer_code, create_referrer_code_in_base, delete_referrer_code_from_base, \
    get_user_referrals_from_base
from src.services.password_service import encrypt_password, check_password
from src.services.token_service import generate_jwt, decode_jwt


async def create_user(user_info):
    user_with_email = await get_user_by_email(user_info.email)
    if user_with_email:
        print("User with such email already exists")
        return None

    referrer_id = None
    if user_info.referrer_code:
        referrer_id_from_base = await get_referrer_by_referrer_code(user_info.referrer_code)
        if not referrer_id_from_base:
            print("The referrer was not found by code.")
            return None
        referrer_id = referrer_id_from_base

    encrypted_password = encrypt_password(user_info.password)
    user_info.password = encrypted_password.decode()
    new_user_id = await create_user_in_base(user_info, referrer_id)
    return new_user_id


async def authenticate_user(email, password):
    user_with_email = await get_user_by_email(email)
    if not user_with_email:
        print("User with such email not exists")
        return None

    is_password_valid = check_password(password, str.encode(user_with_email.password))
    if not is_password_valid:
        return None

    jwt = generate_jwt(user_with_email.id)
    return jwt


async def get_referrer_code_by_email(email):
    user_with_email = await get_user_by_email(email)
    if not user_with_email:
        print("User with such email not exists")
        return None
    referrer_code = await get_referrer_code_by_user_id(user_with_email.id)
    if not referrer_code:
        print("No referrer code in base for user wuth email")
        return None
    if datetime.now().date() >= referrer_code.end_date:
        print("Referrer code expired")
        return None
    return referrer_code.code


async def create_referrer_code(user_token):
    user_id = decode_jwt(user_token)
    if not user_id:
        return None
    referrer_code = generate_referrer_code()
    code_end_date = datetime.now() + timedelta(minutes=int(os.getenv("API_REFERRER_CODE_EXPIRE_MINUTES")))
    await create_referrer_code_in_base(user_id, referrer_code, code_end_date)
    return referrer_code


async def delete_referrer_code_by_token(user_token):
    user_id = decode_jwt(user_token)
    if not user_id:
        return
    await delete_referrer_code_from_base(user_id)


async def get_user_referrals(user_id):
    result = []
    user_referrals = await get_user_referrals_from_base(user_id)
    if user_referrals:
        result = [
            {
                "name": user.name,
                "email": user.email
            } for user in user_referrals]
    return result


def generate_referrer_code():
    letters_and_digits = string.ascii_letters + string.digits
    code = ''.join(random.sample(letters_and_digits, int(os.getenv("API_REFERRER_CODE_LENGTH"))))
    return code
