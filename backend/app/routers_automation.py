from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User, AutomationRequest
from app.schemas import AutomationRequestCreate, AutomationRequestOut
from app.routers_user import get_current_user
import json
import libs.kick as kick
import libs.twitch as twitch
from datetime import datetime

router = APIRouter(prefix="/automation", tags=["automation"])

# Submit automation request
@router.post("/request", response_model=AutomationRequestOut)
async def submit_request(
    req: AutomationRequestCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    # Save request
    db_req = AutomationRequest(
        user_id=current_user.id,
        platform=req.platform,
        feature=req.feature,
        parameters=json.dumps(req.parameters),
        status="pending",
    )
    db.add(db_req)
    await db.commit()
    await db.refresh(db_req)
    # Call automation in background
    if background_tasks:
        background_tasks.add_task(run_automation, db_req.id, req, current_user.id, db)
    else:
        await run_automation(db_req.id, req, current_user.id, db)
    return db_req

# View request history
@router.get("/history", response_model=list[AutomationRequestOut])
async def get_history(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AutomationRequest).where(AutomationRequest.user_id == current_user.id))
    return result.scalars().all()

# Run automation (calls libs)
async def run_automation(request_id, req, user_id, db):
    # This is a simplified dispatcher; expand as needed for all features
    try:
        if req.platform == "kick":
            if req.feature == "follow":
                kick.Follow().unlockAccount(req.parameters["username"], req.parameters["count"])
            elif req.feature == "view":
                kick.View(req.parameters["username"]).Send(
                    req.parameters.get("proxy"),
                    req.parameters["username"],
                    req.parameters["end_time"]
                )
            elif req.feature == "chat":
                kick.Chat().unlockAccount(
                    req.parameters["username"],
                    req.parameters["message"],
                    0, 0.0001, req.parameters["count"]
                )
            elif req.feature == "poll":
                kick.Poll().send_vote(req.parameters["username"], req.parameters["poll_id"])
            elif req.feature == "clip":
                kick.Clip().send_view(req.parameters["clip_id"])
        elif req.platform == "twitch":
            if req.feature == "follow":
                twitch.Follow().send_follow(
                    req.parameters["target_id"],
                    req.parameters["count"],
                    req.parameters.get("tokens")
                )
            elif req.feature == "chat":
                twitch.Chat().send_messages(
                    req.parameters["username"],
                    req.parameters["message"],
                    req.parameters["count"],
                    req.parameters.get("fake", False),
                    req.parameters.get("delay", 0.1)
                )
            elif req.feature == "reaction":
                twitch.Reaction().send_reactions(
                    req.parameters["target_id"],
                    req.parameters["count"],
                    req.parameters["type"],
                    req.parameters["broadcast_id"],
                    req.parameters.get("tokens")
                )
        # Update status
        result = await db.execute(select(AutomationRequest).where(AutomationRequest.id == request_id))
        db_req = result.scalar()
        db_req.status = "completed"
        db_req.updated_at = datetime.utcnow()
        await db.commit()
    except Exception as e:
        result = await db.execute(select(AutomationRequest).where(AutomationRequest.id == request_id))
        db_req = result.scalar()
        db_req.status = f"error: {str(e)}"
        db_req.updated_at = datetime.utcnow()
        await db.commit() 