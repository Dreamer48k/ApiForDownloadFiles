from fastapi import APIRouter

router_users = APIRouter(
    prefix='/users',
    tags=["Users"]
)
