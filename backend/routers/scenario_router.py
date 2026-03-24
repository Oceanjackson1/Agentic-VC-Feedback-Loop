"""场景路由：返回所有可用场景的元数据"""

from fastapi import APIRouter
from prompts import get_all_scenarios_meta

router = APIRouter(prefix="/api", tags=["scenarios"])


@router.get("/scenarios")
def list_scenarios():
    """返回所有可用场景的元数据列表"""
    return get_all_scenarios_meta()
