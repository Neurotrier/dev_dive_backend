from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router
from .tag import router as tag_router
from .question import router as question_router
from .answer import router as answer_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(tag_router)
router.include_router(question_router)
router.include_router(answer_router)
