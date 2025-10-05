from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.models import Transaction, Wallet
import secrets

# Create router instance
router = APIRouter()


# ===== Pydantic Models =====

class TransactionCreate(BaseModel):
    """Schema for creating a new transaction"""
    sender_address: str = Field(..., description="Sender wallet address")
    recipient_address: str = Field(..., description="Recipient wallet address")
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")


class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    id: int
    sender_address: str
    recipient_address: str
    amount: float
    status: str
    transaction_hash: str
    timestamp: str


# ===== Helper Functions =====

def generate_transaction_hash() -> str:
    """
    Generate a mock transaction hash.
    Format: 0x followed by 64 hexadecimal characters

    Returns:
        str: Mock transaction hash
    """
    random_bytes = secrets.token_bytes(32)  # 32 bytes = 64 hex characters
    tx_hash = "0x" + random_bytes.hex()
    return tx_hash


# ===== API Routes =====

@router.post("/send", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def send_transaction(tx_data: TransactionCreate, db: Session = Depends(get_db)):
    """
    Send a transaction from one wallet to another.

    Args:
        tx_data: Transaction details
        db: Database session

    Returns:
        TransactionResponse: Created transaction details

    Raises:
        HTTPException: If sender wallet not found or insufficient balance
    """
    # Verify sender wallet exists
    sender = db.query(Wallet).filter(Wallet.address == tx_data.sender_address).first()
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sender wallet not found"
        )

    # Verify recipient wallet exists
    recipient = db.query(Wallet).filter(Wallet.address == tx_data.recipient_address).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient wallet not found"
        )

    # Check sufficient balance
    if sender.balance < tx_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    # Generate transaction hash
    tx_hash = generate_transaction_hash()

    # Create transaction record
    transaction = Transaction(
        sender_address=tx_data.sender_address,
        recipient_address=tx_data.recipient_address,
        amount=tx_data.amount,
        transaction_hash=tx_hash,
        status="completed"  # Mock: assume all transactions complete immediately
    )

    # Update balances
    sender.balance -= tx_data.amount
    recipient.balance += tx_data.amount

    # Save to database
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return TransactionResponse(
        id=transaction.id,
        sender_address=transaction.sender_address,
        recipient_address=transaction.recipient_address,
        amount=transaction.amount,
        status=transaction.status,
        transaction_hash=transaction.transaction_hash,
        timestamp=transaction.timestamp.isoformat()
    )


@router.get("/history/{address}", response_model=list[TransactionResponse])
async def get_transaction_history(address: str, db: Session = Depends(get_db)):
    """
    Get transaction history for a wallet address.

    Args:
        address: Wallet address
        db: Database session

    Returns:
        list[TransactionResponse]: List of transactions
    """
    # Get transactions where address is sender or recipient
    transactions = db.query(Transaction).filter(
        (Transaction.sender_address == address) | (Transaction.recipient_address == address)
    ).order_by(Transaction.timestamp.desc()).all()

    return [
        TransactionResponse(
            id=tx.id,
            sender_address=tx.sender_address,
            recipient_address=tx.recipient_address,
            amount=tx.amount,
            status=tx.status,
            transaction_hash=tx.transaction_hash,
            timestamp=tx.timestamp.isoformat()
        )
        for tx in transactions
    ]


@router.get("/{tx_hash}", response_model=TransactionResponse)
async def get_transaction(tx_hash: str, db: Session = Depends(get_db)):
    """
    Get transaction details by hash.

    Args:
        tx_hash: Transaction hash
        db: Database session

    Returns:
        TransactionResponse: Transaction details

    Raises:
        HTTPException: If transaction not found
    """
    transaction = db.query(Transaction).filter(Transaction.transaction_hash == tx_hash).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    return TransactionResponse(
        id=transaction.id,
        sender_address=transaction.sender_address,
        recipient_address=transaction.recipient_address,
        amount=transaction.amount,
        status=transaction.status,
        transaction_hash=transaction.transaction_hash,
        timestamp=transaction.timestamp.isoformat()
    )