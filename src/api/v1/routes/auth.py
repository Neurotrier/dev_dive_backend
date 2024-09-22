from fastapi import APIRouter, status, HTTPException

from src.domain.schemas.auth import AuthSignup
from src.db.session import DBSession
from src.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def signup(
    data: AuthSignup,
    db: DBSession,
):
    _service = UserService(session=db)
    try:
        response = await _service.create_user(data=data)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
