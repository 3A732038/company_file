# routers/notifications.py
from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# In-memory storage for notifications (for demo purposes)
notifications_db = {}
notification_id_counter = 1

class Notification(BaseModel):
    id: Optional[int] = None
    user_id: int
    message: str
    read: bool = False

@router.get("")
async def get_all_notifications():
    """Get all notifications"""
    return {"notifications": list(notifications_db.values())}

@router.get("/{user_id}")
async def get_user_notifications(user_id: int):
    """Get notifications for a specific user"""
    user_notifications = [
        notif for notif in notifications_db.values() 
        if notif["user_id"] == user_id
    ]
    return {"user_id": user_id, "notifications": user_notifications}

@router.post("")
async def create_notification(notification: Notification):
    """Create a new notification"""
    global notification_id_counter
    
    notification.id = notification_id_counter
    notifications_db[notification_id_counter] = notification.dict()
    notification_id_counter += 1
    
    return {"message": "Notification created successfully", "notification": notification}

@router.put("/{notification_id}/read")
async def mark_notification_as_read(notification_id: int):
    """Mark a notification as read"""
    if notification_id not in notifications_db:
        return {"error": "Notification not found"}, 404
    
    notifications_db[notification_id]["read"] = True
    return {"message": "Notification marked as read", "notification": notifications_db[notification_id]}

@router.delete("/{notification_id}")
async def delete_notification(notification_id: int):
    """Delete a notification"""
    if notification_id not in notifications_db:
        return {"error": "Notification not found"}, 404
    
    deleted_notification = notifications_db.pop(notification_id)
    return {"message": "Notification deleted successfully", "notification": deleted_notification}
