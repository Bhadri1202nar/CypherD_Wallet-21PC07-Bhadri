from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.models import Wallet
import secrets
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create router instance
router = APIRouter()

# Security scheme
security = HTTPBearer()

# JWT Configuration from environment
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# ===== Pydantic Models (Request/Response schemas) =====

class WalletCreate(BaseModel):
    """Schema for creating a new wallet"""
    password: str = Field(..., min_length=6, description="Password for wallet (min 6 characters)")


class WalletLogin(BaseModel):
    """Schema for wallet login"""
    address: str
    password: Optional[str] = None


class WalletImport(BaseModel):
    """Schema for importing existing wallet"""
    address: str = Field(..., description="Wallet address (0x...)")
    private_key: str = Field(..., description="Private key")


class WalletResponse(BaseModel):
    """Schema for wallet response"""
    address: str
    balance: float
    private_key: str
    message: str = "Wallet created successfully"


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    address: str
    balance: float


# ===== Helper Functions =====

def generate_wallet_address() -> str:
    """
    Generate a mock Ethereum-style wallet address.
    Format: 0x followed by 40 hexadecimal characters
    
    Returns:
        str: Mock wallet address (e.g., 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1)
    """
    random_bytes = secrets.token_bytes(20)  # 20 bytes = 40 hex characters
    address = "0x" + random_bytes.hex()
    return address


def generate_private_key() -> str:
    """
    Generate a mock private key.
    Format: 64 hexadecimal characters
    
    Returns:
        str: Mock private key
    """
    random_bytes = secrets.token_bytes(32)  # 32 bytes = 64 hex characters
    private_key = random_bytes.hex()
    return private_key


def hash_password(password: str) -> str:
    """
    Hash password using SHA256.
    Note: In production, use proper password hashing like bcrypt or argon2!

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token.

    Args:
        data: Data to encode in token
        expires_delta: Optional expiration time

    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token and return wallet address.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        str: Wallet address from token

    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        wallet_address: str = payload.get("sub")
        if wallet_address is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return wallet_address
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_wallet(wallet_address: str = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Dependency to get current authenticated wallet.

    Args:
        wallet_address: Wallet address from token
        db: Database session

    Returns:
        Wallet: Wallet object

    Raises:
        HTTPException: If wallet not found
    """
    wallet = db.query(Wallet).filter(Wallet.address == wallet_address).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return wallet


# ===== API Routes =====

@router.post("/register", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
async def register_wallet(wallet_data: WalletCreate, db: Session = Depends(get_db)):
    """
    Create a new wallet with generated address and private key.
    
    Args:
        wallet_data: Password for the wallet
        db: Database session
        
    Returns:
        WalletResponse: New wallet details including address, balance, and private key
        
    Raises:
        HTTPException: If wallet creation fails
    """
    # Generate unique wallet credentials
    address = generate_wallet_address()
    private_key = generate_private_key()
    
    # Check if address already exists (unlikely but good practice)
    existing = db.query(Wallet).filter(Wallet.address == address).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Wallet already exists (collision detected)"
        )
    
    # Create new wallet in database
    wallet = Wallet(
        address=address,
        private_key=private_key,
        balance=3.34  # Initial balance: 3.34 ETH
    )
    
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    
    return WalletResponse(
        address=wallet.address,
        balance=wallet.balance,
        private_key=wallet.private_key,
        message="Wallet created successfully! Save your private key securely."
    )


@router.post("/login", response_model=TokenResponse)
async def login_wallet(wallet_data: WalletLogin, db: Session = Depends(get_db)):
    """
    Login to existing wallet using address and return JWT token.

    Args:
        wallet_data: Wallet address and password
        db: Database session

    Returns:
        TokenResponse: JWT access token and wallet info

    Raises:
        HTTPException: If wallet not found
    """
    # Find wallet by address
    wallet = db.query(Wallet).filter(Wallet.address == wallet_data.address).first()

    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    # In a real app, you would verify the password here
    # For this mock, we just authenticate with the address

    # Create access token
    access_token = create_access_token(data={"sub": wallet.address})

    return TokenResponse(
        access_token=access_token,
        address=wallet.address,
        balance=wallet.balance
    )


@router.post("/import")
async def import_wallet(wallet_data: WalletImport, db: Session = Depends(get_db)):
    """
    Import existing wallet using address and private key.
    
    Args:
        wallet_data: Wallet address and private key
        db: Database session
        
    Returns:
        dict: Import confirmation and wallet details
    """
    # Check if wallet already exists in database
    existing = db.query(Wallet).filter(Wallet.address == wallet_data.address).first()
    
    if existing:
        # Wallet already in database
        return {
            "address": existing.address,
            "balance": existing.balance,
            "message": "Wallet already exists and has been loaded"
        }
    
    # Import new wallet into database
    wallet = Wallet(
        address=wallet_data.address,
        private_key=wallet_data.private_key,
        balance=3.34  # Default balance for imported wallets
    )
    
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    
    return {
        "address": wallet.address,
        "balance": wallet.balance,
        "message": "Wallet imported successfully"
    }


@router.get("/verify/{address}")
async def verify_wallet(address: str, db: Session = Depends(get_db)):
    """
    Verify if a wallet address exists in the system.
    
    Args:
        address: Wallet address to verify
        db: Database session
        
    Returns:
        dict: Verification status
    """
    wallet = db.query(Wallet).filter(Wallet.address == address).first()
    
    return {
        "exists": wallet is not None,
        "address": address
    }