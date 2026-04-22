from typing import Any, List

from fastapi.security import HTTPBearer
from fastapi import Depends, Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio.session import AsyncSession

from FastAPI.Ssali_Jonathan.CRUD.auth.user_models import User
from FastAPI.Ssali_Jonathan.CRUD.auth.user_service import UserService
from FastAPI.Ssali_Jonathan.CRUD.core.database import get_session
from FastAPI.Ssali_Jonathan.CRUD.core.redis import add_jti_to_blocklist, token_in_blocklist
from FastAPI.Ssali_Jonathan.CRUD.utils.utils import decode_token

from FastAPI.Ssali_Jonathan.CRUD.core.errors import AccountNotVerified, InvalidToken, AccessTokenRequired, RefreshTokenRequired, InsufficientPermission

user_service = UserService()


class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error = auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        
        creds = await super().__call__(request)
        # print(creds.scheme)
        # print(creds.credentials)
 
        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail = {
            #         "error": "This token is invalid or expired",
            #         "resolution": "Please get new token"
            #     }
            # )
            raise InvalidToken()
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail = {
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token"
                }
            )

        self.verify_token_data(token_data)

        return token_data
    

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        # if token_data is not None:
        #     return True
        # else:
        #     return False

        return token_data is not None
    
    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail="Please provide an access token"
            # )
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail="Please provide a refresh token"
            # )
            raise RefreshTokenRequired()

async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
    ):
    user_email = token_details['user']['email']

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:

        self.allowed_roles = allowed_roles

    
    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:

        if not current_user.is_verified:
            raise AccountNotVerified()
        
        if current_user.role in self.allowed_roles:
            return True
        
        # raise HTTPException(
        #     status_code = status.HTTP_403_FORBIDDEN,
        #     detail = "You are not allowed to perform this action"
        # )
        raise InsufficientPermission()