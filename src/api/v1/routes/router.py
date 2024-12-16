from fastapi import APIRouter

from .answer import router as answer_router
from .auth import router as auth_router
from .chat import router as chat_router
from .image import router as image_router
from .question import router as question_router
from .tag import router as tag_router
from .user import router as user_router
from .vote import router as vote_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(tag_router)
router.include_router(question_router)
router.include_router(answer_router)
router.include_router(vote_router)
router.include_router(chat_router)
router.include_router(image_router)
