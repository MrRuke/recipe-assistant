from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..database import sqlite_conn
from ..schemas import UserSettingsSchema

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("", response_model=UserSettingsSchema)
async def get_settings():
    """Return the single user's profile settings."""
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute(
            "SELECT height_cm, weight_kg, goal FROM user_settings WHERE id = 1"
        )
        row = cursor.fetchone()
        if row is None:
            # Fallback — should never happen after init, but be safe
            return UserSettingsSchema()
        return UserSettingsSchema(
            height_cm=row[0],
            weight_kg=row[1],
            goal=row[2],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения настроек: {str(e)}")


@router.put("", response_model=UserSettingsSchema)
async def update_settings(settings: UserSettingsSchema):
    """Persist the single user's profile settings."""
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute(
            """
            UPDATE user_settings
            SET height_cm = ?, weight_kg = ?, goal = ?, updated_at = ?
            WHERE id = 1
            """,
            (settings.height_cm, settings.weight_kg, settings.goal, datetime.utcnow()),
        )
        sqlite_conn.commit()
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения настроек: {str(e)}")
