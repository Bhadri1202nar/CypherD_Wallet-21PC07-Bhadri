import { useState, useEffect } from 'react';
import { walletAPI } from '@/lib/api';

export default function WalletCard({ address, onLogout }) {
  const [walletInfo, setWalletInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (address) {
      loadWalletInfo();
    }
  }, [address]);

  const loadWalletInfo = async () => {
    try {
      setLoading(true);
      const info = await walletAPI.getInfo(address);
      setWalletInfo(info);
      setError(null);
    } catch (err) {
      setError('Failed to load wallet info');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={loadWalletInfo}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-xl font-bold text-gray-800">Wallet</h2>
        <button
          onClick={onLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
        >
          Logout
        </button>
      </div>

      <div className="space-y-3">
        <div>
          <label className="text-sm font-medium text-gray-600">Address</label>
          <p className="font-mono text-sm bg-gray-100 p-2 rounded break-all">
            {walletInfo?.address}
          </p>
        </div>

        <div>
          <label className="text-sm font-medium text-gray-600">Balance</label>
          <p className="text-2xl font-bold text-green-600">
            {walletInfo?.balance?.toFixed(4)} ETH
          </p>
        </div>

        <div>
          <label className="text-sm font-medium text-gray-600">Created</label>
          <p className="text-sm text-gray-500">
            {walletInfo?.created_at ? new Date(walletInfo.created_at).toLocaleDateString() : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  );
}