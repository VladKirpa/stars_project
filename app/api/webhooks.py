from fastapi import APIRouter, Depends

from app.database import get_db
from app.schemas.finances import UserLeaveRequest
from app.schemas.admin import StatusResponse
from app.orm.procces_leave_orm import process_user_leave

router = APIRouter(prefix="/webhooks", tags=["System Webhooks"])

@router.post("/telegram/leave", response_model=StatusResponse)
async def api_user_leave(data: UserLeaveRequest, session = Depends(get_db)):
    result = await process_user_leave(data.user_id, data.order_id, session)
    if not result:
        return StatusResponse(message="Ignored: Task completion not found or already canceled")
    return StatusResponse(message=result["message"])