Mock Web3 Wallet
A full-stack mock Web3 wallet application built with FastAPI (backend) and Next.js (frontend). This project simulates core wallet functionality including balance management, transactions, and real-time notifications. 🚀

## Features

### Frontend (What the User Sees)
- Create or Import Wallet: Generate a new wallet or import existing
- View Balance: Display current balance in mock ETH
- Approve Transactions: Sign and confirm transactions
- Transaction History: View past activity with timestamps

### Backend (The Engine Room)
- Manage Wallet Data: Store user balances in database
- Handle User Operations: Process transactions (0.01-0.05 USD)
- Security Verifications: Validate transactions and signatures
- Process Transfers: Update balances after transactions
- Send Notifications: Alert users about transaction status

## 🛠️ Setup Instructions

### Backend Setup
1. Navigate to backend directory:
    ```bash
    cd backend
    ```
2. Create virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create .env file:
    ```env
    DATABASE_URL=sqlite:///./wallet.db
    SECRET_KEY=your-secret-key-here-change-in-production
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. Run the backend:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    Backend will be available at http://localhost:8000  
    API documentation at http://localhost:8000/docs

### Frontend Setup
1. Navigate to frontend directory:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Create .env.local file:
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```
4. Run the development server:
    ```bash
    npm run dev
    ```
    Frontend will be available at http://localhost:3000

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new wallet
- `POST /auth/login` - Login with wallet address

### Wallet Operations
- `GET /wallet/balance` - Get current balance
- `POST /wallet/create` - Create new wallet

### Transactions
- `POST /transactions/send` - Send transaction
- `GET /transactions/history` - Get transaction history
- `POST /transactions/approve` - Approve pending transaction

### Notifications
- `GET /notifications` - Get user notifications
- `WebSocket /ws/{wallet_address}` - Real-time notifications

## 🧪 Testing the Application
1. **Create a Wallet:**
   - Open the frontend
   - Click "Create Wallet"
   - Save your generated wallet address
2. **Check Balance:**
   - Your initial balance will be 3.34 ETH
3. **Send a Transaction:**
   - Enter recipient address
   - Enter amount (between 0.01-0.05 ETH)
   - Click "Send"
   - View transaction in history
4. **View Notifications:**
   - Receive real-time updates on transactions
   - See confirmation messages

## 🔒 Security Notes
- This is a MOCK wallet for educational purposes
- Do NOT use with real cryptocurrency or private keys
- Private keys are stored in a local database (SQLite)
- Not suitable for production use

## 📦 Technologies Used

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- SQLite - Lightweight database
- Pydantic - Data validation
- WebSockets - Real-time communication

### Frontend
- Next.js 14 - React framework with App Router
- TypeScript - Type-safe JavaScript
- Tailwind CSS - Utility-first CSS framework
- Lucide React - Icon library

## 🎯 Learning Objectives
- Understand Web3 wallet architecture
- Learn backend API design with FastAPI
- Practice React/Next.js frontend development
- Implement real-time features with WebSockets
- Handle user authentication and authorization

## 🐛 Troubleshooting
### Backend won't start:
- Check if port 8000 is available
- Ensure all dependencies are installed
- Verify Python version (3.8+)

### Frontend won't connect:
- Verify backend is running
- Check NEXT_PUBLIC_API_URL in .env.local
- Clear browser cache

### Database errors:
- Delete wallet.db and restart backend
- Check file permissions

## 📝 License
MIT License - Feel free to use for educational purposes

## 🤝 Contributing
This is an educational project. Feel free to fork and experiment!

**Happy Building! 🚀**
