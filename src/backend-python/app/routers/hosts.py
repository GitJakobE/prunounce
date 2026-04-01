from fastapi import APIRouter

from ..hosts import HOSTS


router = APIRouter(prefix="/api/hosts")


@router.get("")
def list_hosts() -> dict:
    return {"hosts": HOSTS}
