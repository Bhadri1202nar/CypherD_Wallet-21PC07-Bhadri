from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Wallet

# Create router instance
router = APIRouter()


# ===== Pydantic Models =====

class WalletInfo(BaseModel):
    """Schema for wallet information response"""
    address: str
    balance: float
    created_at: str


# ===== API Routes =====

@router.get("/balance/{address}", response_model=dict)
async def get_wallet_balance(address: str, db: Session = Depends(get_db)):
    """
    Get wallet balance by address.

    Args:
        address: Wallet address
        db: Database session

    Returns:
        dict: Wallet balance information

    Raises:
        HTTPException: If wallet not found
    """
    wallet = db.query(Wallet).filter(Wallet.address == address).first()

    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    return {
        "address": wallet.address,
        "balance": wallet.balance
    }


@router.get("/info/{address}", response_model=WalletInfo)
async def get_wallet_info(address: str, db: Session = Depends(get_db)):
    """
    Get complete wallet information by address.

    Args:
        address: Wallet address
        db: Database session

    Returns:
        WalletInfo: Complete wallet information

    Raises:
        HTTPException: If wallet not found
    """
    wallet = db.query(Wallet).filter(Wallet.address == address).first()

    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    return WalletInfo(
        address=wallet.address,
        balance=wallet.balance,
        created_at=wallet.created_at.isoformat()
    )