from sqlalchemy.ext.asyncio.session import AsyncSession

from datetime import timedelta, datetime

from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, BackgroundTasks, Depends, status

from FastAPI.Ssali_Jonathan.CRUD.core.celery_tasks import send_email
from FastAPI.Ssali_Jonathan.CRUD.core.config import get_settings
from FastAPI.Ssali_Jonathan.CRUD.core.database import get_session
from FastAPI.Ssali_Jonathan.CRUD.core.mail import create_message, mail
from FastAPI.Ssali_Jonathan.CRUD.core.redis import add_jti_to_blocklist
from FastAPI.Ssali_Jonathan.CRUD.auth.user_schema import PasswordResetConfirmModel, PasswordResetRequestModel, UserBooksModel, UserCreateModel, UserResponse, UserLoginModel, EmailModel
from FastAPI.Ssali_Jonathan.CRUD.auth.user_service import UserService
from FastAPI.Ssali_Jonathan.CRUD.utils.utils import create_access_token, decode_token, verify_password, create_url_safe_token, decode_url_safe_token, generate_paswd_hash
from FastAPI.Ssali_Jonathan.CRUD.utils.dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker
from FastAPI.Ssali_Jonathan.CRUD.core.errors import UserAlreadyExists, InvalidCredentials, InvalidToken, UserNotFound

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = 2

settings = get_settings()

@auth_router.post('/send_mail')
async def send_mail(emails: EmailModel):
    emails = emails.email_addr

    # print("USERNAME:", settings.mail_username)
    # print("PASSWORD:", settings.mail_password)

    html = "<h1> Welcome to the App </h1>"
    subject = "Welcome to the App"

    # message = create_message(
    #     recipients = emails,
    #     subject = "Welcome",
    #     body = html
    # )

    # await mail.send_message(message)

    send_email.delay(emails, subject, html)

    return {"message" : "Email Sent Successfully"}



@auth_router.post('/signup', 
    # response_model = UserResponse, 
    status_code = status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")
        raise UserAlreadyExists()
    
    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token(
        {"email": email}
    )

    link = f"http://{settings.domain}/api/v1/auth/verify/{token}"

    html_message = f"""
        <h1> Verify your Email</h1>
        <p> Please click this <a href="{link}">link</a> to verify yout email</p>
    """

    # message = create_message(
    #     recipients = [email],
    #     subject = "Verify your email",
    #     body = html_message
    # )

    # # await mail.send_message(message)
    
    # ## with BackgroundTasks
    # bg_tasks.add_task(mail.send_message, message)

    emails = [email]

    subject = "Verify your email"


    send_email.delay(emails, subject, html_message)


    return {
        "message" : "Accounted Created! Check email to verify your account",
        "user" : new_user
    }


@auth_router.get('/verify/{token}')
async def verify_user_accounts(
    token: str,
    session: AsyncSession = Depends(get_session)
):
    token_data = decode_url_safe_token(token)

    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {'is_verified': True}, session)

        return JSONResponse(
            content={
                "message" : "Account verified succesfully",
            },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content = {
            "message" : "Error occured during verification"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

 
@auth_router.post('/login')
async def login_users(user_login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_login_data.email
    password = user_login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uuid': str(user.uid),
                    'role': user.role
                }
            )

            refresh_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uuid': str(user.uid) 
                },
                refresh = True,
                expiry = timedelta(days = REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content = {
                    "message" : "Login Successful",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "user" : {
                        "email": user.email,
                        "uid" : str(user.uid) 
                    }
                }
            )
    
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Invalid Email or password"
    # )
    raise InvalidCredentials()


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):

    expiry_timestamp = token_details['exp']
    # print(expiry_timestamp)

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token( 
            user_data=token_details['user']
        )

        return JSONResponse(
            content = {
                "access_token": new_access_token
            }
        )

    # raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST,
    #     details="Invalid or expired token"
    # )
    raise InvalidToken()


@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(
    user = Depends(get_current_user),
    _: bool = Depends(role_checker)
):
    return user


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse (
        content = {
            "message": "logged out successfully",
        },
        status_code=status.HTTP_200_OK
    )



"""
1. Provide The Email -> password reset request
2. Send Password Reset Link
3. Reset Password -> password reset confirm
"""


@auth_router.post('/password-reset-request')
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token(
        {"email": email}
    )

    link = f"http://{settings.domain}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
        <h1>Reset your Password</h1>
        <p> Please click this <a href="{link}">link</a> to reset your password</p>
    """

    message = create_message(
        recipients = [email],
        subject = "Reset your password",
        body = html_message
    )

    await mail.send_message(message)

    # return {
    #     "message" : "Please check your email for instructions to reset your password"
    # }
    
    return JSONResponse(
        content = {
            "message" : "Please check your email for instructions to reset your password"
        },
        status_code = status.HTTP_200_OK
    )


@auth_router.post('/password-reset-confirm/{token}')
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session)
):
    new_password = passwords.new_password
    confirm_new_password = passwords.confirm_new_password

    if new_password != confirm_new_password:
        raise HTTPException(
            detail = "Passwords do not match",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    
    token_data = decode_url_safe_token(token)

    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()
        
        password_hash = generate_paswd_hash(new_password)

        await user_service.update_user(user, {'password_hash': password_hash}, session)

        return JSONResponse(
            content={
                "message" : "Password reset succesfully",
            },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content = {
            "message" : "Error occured during password reset"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )