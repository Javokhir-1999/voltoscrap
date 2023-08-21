from fastapi import APIRouter

from application.controllers import comment_controller, search_controller,post_controller

public_router = APIRouter()
# register public controllers here
public_router.include_router(prefix="/search", router=search_controller.router, tags=["Search"])
public_router.include_router(prefix="/post", router=post_controller.router, tags=["Post"])
public_router.include_router(prefix="/comment", router=comment_controller.router, tags=["Comment"])
