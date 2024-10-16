from typing import Annotated
from fastapi import FastAPI, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer

from src.services.serializers import SignUp, LogIn, validate_email
from src.services.main_service import create_user, authenticate_user, create_referrer_code, \
    get_referrer_code_by_email, delete_referrer_code_by_token, get_user_referrals


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


@app.post("/auth/signup/", status_code=201)
async def signup_user(signup_user_info: SignUp, response: Response):
    try:
        is_email_valid = validate_email(signup_user_info.email)
        if not is_email_valid:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Invalid email"}
        user_id = await create_user(signup_user_info)
        if not user_id:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "User was not created"}
        return {"user_id": str(user_id)}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@app.post("/auth/login/", status_code=200)
async def login_user(login_user_info: LogIn, response: Response):
    try:
        is_email_valid = validate_email(login_user_info.email)
        if not is_email_valid:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Invalid email"}
        token = await authenticate_user(login_user_info.email, login_user_info.password)
        if not token:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"detail": "Not authenticated"}

        return {"token": token}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@app.get("/referrer_code/", status_code=200)
async def get_referrer_code(email: str, response: Response):
    try:
        email = email
        is_email_valid = validate_email(email)
        if not is_email_valid:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Invalid email"}
        referrer_code = await get_referrer_code_by_email(email)
        if not referrer_code:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "No referrer code for this email."}
        return {"referrer_code": referrer_code}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@app.post("/referrer_code/", status_code=201)
async def create_new_referrer_code(token: Annotated[str, Depends(oauth2_scheme)], response: Response):
    try:
        new_referrer_code = await create_referrer_code(token)
        if not new_referrer_code:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "New referrer code not created."}
        return {"referrer_code": new_referrer_code}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@app.delete("/referrer_code/", status_code=204)
async def delete_referrer_code(token: Annotated[str, Depends(oauth2_scheme)], response: Response):
    try:
        await delete_referrer_code_by_token(token)
        return {"detail": "Code deleted."}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@app.get("/referral/", status_code=200)
async def get_referrals(user_id: str, response: Response):
    try:
        user_id = user_id
        user_referrals = await get_user_referrals(user_id)
        return {"user_referrals": user_referrals}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}
