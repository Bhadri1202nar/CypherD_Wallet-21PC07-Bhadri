from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Wallet(Base):
    """Wallet model - stores wallet information"""
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True, nullable=False)
    private_key = Column(String, nullable=False)  # In production, encrypt this!
    balance = Column(Float, default=3.34)  # Initial balance in ETH
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions_sent = relationship(
        "Transaction", 
        foreign_keys="Transaction.sender_address", 
        back_populates="sender"
    )
    transactions_received = relationship(
        "Transaction", 
        foreign_keys="Transaction.recipient_address", 
        back_populates="recipient"
    )
    notifications = relationship("Notification", back_populates="wallet")


class Transaction(Base):
    """Transaction model - stores all wallet transactions"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_address = Column(String, ForeignKey("wallets.address"), nullable=False)
    recipient_address = Column(String, ForeignKey("wallets.address"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    transaction_hash = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship(
        "Wallet", 
        foreign_keys=[sender_address], 
        back_populates="transactions_sent"
    )
    recipient = relationship(
        "Wallet", 
        foreign_keys=[recipient_address], 
        back_populates="transactions_received"
    )


class Notification(Base):
    """Notification model - stores user notifications"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, ForeignKey("wallets.address"), nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)  # success, error, info, warning
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    wallet = relationship("Wallet", back_populates="notifications")