'use client';

import { useState, useEffect } from 'react';
import { authAPI } from '@/lib/api';
import WalletCard from '@/components/WalletCard';
import TransactionForm from '@/components/TransactionForm';
import TransactionHistory from '@/components/TransactionHistory';
import NotificationPanel from '@/components/NotificationPanel';

export default function Home() {
  const [currentWallet, setCurrentWallet] = useState(null);
  const [authMode, setAuthMode] = useState('login'); // login, register, import
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form states
  const [loginAddress, setLoginAddress] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [importAddress, setImportAddress] = useState('');
  const [importPrivateKey, setImportPrivateKey] = useState('');

  useEffect(() => {
    // Check if wallet is stored in localStorage
    const storedWallet = localStorage.getItem('currentWallet');
    if (storedWallet) {
      setCurrentWallet(JSON.parse(storedWallet));
    }
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!loginAddress) {
      setError('Please enter wallet address');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const result = await authAPI.login(loginAddress);

      if (result.detail) {
        throw new Error(result.detail);
      }

      const wallet = { address: result.address, balance: result.balance };
      setCurrentWallet(wallet);
      localStorage.setItem('currentWallet', JSON.stringify(wallet));
      setSuccess('Logged in successfully!');
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!registerPassword) {
      setError('Please enter a password');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const result = await authAPI.register(registerPassword);

      if (result.detail) {
        throw new Error(result.detail);
      }

      const wallet = { address: result.address, balance: result.balance };
      setCurrentWallet(wallet);
      localStorage.setItem('currentWallet', JSON.stringify(wallet));
      setSuccess('Wallet created successfully! Save your private key: ' + result.private_key);
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async (e) => {
    e.preventDefault();
    if (!importAddress || !importPrivateKey) {
      setError('Please fill in all fields');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const result = await authAPI.import(importAddress, importPrivateKey);

      if (result.detail) {
        throw new Error(result.detail);
      }

      const wallet = { address: result.address, balance: result.balance };
      setCurrentWallet(wallet);
      localStorage.setItem('currentWallet', JSON.stringify(wallet));
      setSuccess('Wallet imported successfully!');
    } catch (err) {
      setError(err.message || 'Import failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setCurrentWallet(null);
    localStorage.removeItem('currentWallet');
    setLoginAddress('');
    setRegisterPassword('');
    setImportAddress('');
    setImportPrivateKey('');
    setError(null);
    setSuccess(null);
  };

  const handleTransactionSent = () => {
    // Refresh wallet balance and transaction history
    // This will trigger re-fetch in components
  };

  if (currentWallet) {
    return (
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Mock Web3 Wallet</h1>
            <p className="text-gray-600">Manage your crypto assets</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <WalletCard address={currentWallet.address} onLogout={handleLogout} />
            </div>

            <div className="lg:col-span-2 space-y-8">
              <TransactionForm
                senderAddress={currentWallet.address}
                onTransactionSent={handleTransactionSent}
              />
              <TransactionHistory address={currentWallet.address} />
            </div>
          </div>

          <div className="mt-8">
            <NotificationPanel walletAddress={currentWallet.address} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Mock Web3 Wallet
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {authMode === 'login' && 'Sign in to your wallet'}
            {authMode === 'register' && 'Create a new wallet'}
            {authMode === 'import' && 'Import existing wallet'}
          </p>
        </div>

        <div className="flex justify-center space-x-4 mb-8">
          <button
            onClick={() => setAuthMode('login')}
            className={`px-4 py-2 rounded ${authMode === 'login' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Login
          </button>
          <button
            onClick={() => setAuthMode('register')}
            className={`px-4 py-2 rounded ${authMode === 'register' ? 'bg-blue-600 text-white' : 'bg-blue-200 text-gray-700'}`}
          >
            Register
          </button>
          <button
            onClick={() => setAuthMode('import')}
            className={`px-4 py-2 rounded ${authMode === 'import' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Import
          </button>
        </div>

        {authMode === 'login' && (
          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Wallet Address</label>
              <input
                type="text"
                value={loginAddress}
                onChange={(e) => setLoginAddress(e.target.value)}
                placeholder="0x..."
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>
        )}

        {authMode === 'register' && (
          <form onSubmit={handleRegister} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                value={registerPassword}
                onChange={(e) => setRegisterPassword(e.target.value)}
                placeholder="Enter password (min 6 characters)"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-green-400"
            >
              {loading ? 'Creating...' : 'Create Wallet'}
            </button>
          </form>
        )}

        {authMode === 'import' && (
          <form onSubmit={handleImport} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Wallet Address</label>
              <input
                type="text"
                value={importAddress}
                onChange={(e) => setImportAddress(e.target.value)}
                placeholder="0x..."
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Private Key</label>
              <input
                type="text"
                value={importPrivateKey}
                onChange={(e) => setImportPrivateKey(e.target.value)}
                placeholder="64 character hex string"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:bg-purple-400"
            >
              {loading ? 'Importing...' : 'Import Wallet'}
            </button>
          </form>
        )}

        {error && (
          <div className="text-red-600 text-sm text-center bg-red-50 p-3 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="text-green-600 text-sm text-center bg-green-50 p-3 rounded">
            {success}
          </div>
        )}
      </div>
    </div>
  );
}