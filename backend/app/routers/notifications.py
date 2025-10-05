from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Notification

# Create router instance
router = APIRouter()


# ===== Pydantic Models =====

class NotificationResponse(BaseModel):
    """Schema for notification response"""
    id: int
    wallet_address: str
    message: str
    type: str
    read: bool
    created_at: str


class NotificationCreate(BaseModel):
    """Schema for creating a notification"""
    wallet_address: str
    message: str
    type: str  # success, error, info, warning


# ===== API Routes =====

@router.get("/{wallet_address}", response_model=list[NotificationResponse])
async def get_wallet_notifications(wallet_address: str, db: Session = Depends(get_db)):
    """
    Get all notifications for a wallet address.

    Args:
        wallet_address: Wallet address
        db: Database session

    Returns:
        list[NotificationResponse]: List of notifications
    """
    notifications = db.query(Notification).filter(
        Notification.wallet_address == wallet_address
    ).order_by(Notification.created_at.desc()).all()

    return [
        NotificationResponse(
            id=notification.id,
            wallet_address=notification.wallet_address,
            message=notification.message,
            type=notification.type,
            read=notification.read,
            created_at=notification.created_at.isoformat()
        )
        for notification in notifications
    ]


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    """
    Mark a notification as read.

    Args:
        notification_id: Notification ID
        db: Database session

    Returns:
        NotificationResponse: Updated notification

    Raises:
        HTTPException: If notification not found
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.read = True
    db.commit()
    db.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        wallet_address=notification.wallet_address,
        message=notification.message,
        type=notification.type,
        read=notification.read,
        created_at=notification.created_at.isoformat()
    )


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(notification_data: NotificationCreate, db: Session = Depends(get_db)):
    """
    Create a new notification.

    Args:
        notification_data: Notification details
        db: Database session

    Returns:
        NotificationResponse: Created notification
    """
    notification = Notification(
        wallet_address=notification_data.wallet_address,
        message=notification_data.message,
        type=notification_data.type
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        wallet_address=notification.wallet_address,
        message=notification.message,
        type=notification.type,
        read=notification.read,
        created_at=notification.created_at.isoformat()
    )


@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """
    Delete a notification.

    Args:
        notification_id: Notification ID
        db: Database session

    Raises:
        HTTPException: If notification not found
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()

    return {"message": "Notification deleted successfully"}