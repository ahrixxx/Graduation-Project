from fastapi import APIRouter, Depends
from common.database import get_db
from common.dependencies import get_current_user
from sector.service.sector_service import get_sector_overview

router = APIRouter(prefix="/api")


@router.get("/sector-overview")
def sector_overview(
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    sectors = get_sector_overview(db, user.id)
    return {
        "count": len(sectors),
        "sectors": sectors,
    }
