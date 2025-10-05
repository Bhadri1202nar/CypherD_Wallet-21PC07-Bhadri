const API_BASE_URL = 'http://localhost:8000';

// Auth API
export const authAPI = {
  register: async (password) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ password }),
    });
    return response.json();
  },

  login: async (address) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ address, password: "" }),
    });
    return response.json();
  },

  import: async (address, privateKey) => {
    const response = await fetch(`${API_BASE_URL}/auth/import`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ address, private_key: privateKey }),
    });
    return response.json();
  },

  verify: async (address) => {
    const response = await fetch(`${API_BASE_URL}/auth/verify/${address}`);
    return response.json();
  },
};

// Wallet API
export const walletAPI = {
  getBalance: async (address) => {
    const response = await fetch(`${API_BASE_URL}/wallet/balance/${address}`);
    return response.json();
  },

  getInfo: async (address) => {
    const response = await fetch(`${API_BASE_URL}/wallet/info/${address}`);
    return response.json();
  },
};

// Transactions API
export const transactionsAPI = {
  send: async (senderAddress, recipientAddress, amount) => {
    const response = await fetch(`${API_BASE_URL}/transactions/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sender_address: senderAddress,
        recipient_address: recipientAddress,
        amount: parseFloat(amount),
      }),
    });
    return response.json();
  },

  getHistory: async (address) => {
    const response = await fetch(`${API_BASE_URL}/transactions/history/${address}`);
    return response.json();
  },

  getTransaction: async (txHash) => {
    const response = await fetch(`${API_BASE_URL}/transactions/${txHash}`);
    return response.json();
  },
};

// Notifications API
export const notificationsAPI = {
  getWalletNotifications: async (walletAddress) => {
    const response = await fetch(`${API_BASE_URL}/notifications/${walletAddress}`);
    return response.json();
  },

  markAsRead: async (notificationId) => {
    const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
      method: 'PUT',
    });
    return response.json();
  },

  create: async (walletAddress, message, type) => {
    const response = await fetch(`${API_BASE_URL}/notifications/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        wallet_address: walletAddress,
        message,
        type,
      }),
    });
    return response.json();
  },

  delete: async (notificationId) => {
    const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}`, {
      method: 'DELETE',
    });
    return response.json();
  },
};