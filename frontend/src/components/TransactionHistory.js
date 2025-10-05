import { useState, useEffect } from 'react';
import { transactionsAPI } from '@/lib/api';

export default function TransactionHistory({ address }) {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (address) {
      loadTransactions();
    }
  }, [address]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const txs = await transactionsAPI.getHistory(address);
      setTransactions(txs);
      setError(null);
    } catch (err) {
      setError('Failed to load transactions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatAddress = (addr) => {
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
  };

  const getTransactionType = (tx) => {
    if (tx.sender_address === address) {
      return { type: 'Sent', color: 'text-red-600', sign: '-' };
    } else {
      return { type: 'Received', color: 'text-green-600', sign: '+' };
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Transaction History</h2>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Transaction History</h2>
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={loadTransactions}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">Transaction History</h2>
        <button
          onClick={loadTransactions}
          className="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm"
        >
          Refresh
        </button>
      </div>

      {transactions.length === 0 ? (
        <p className="text-gray-500 text-center py-8">No transactions found</p>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {transactions.map((tx) => {
            const txType = getTransactionType(tx);
            return (
              <div key={tx.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center space-x-2">
                    <span className={`font-medium ${txType.color}`}>
                      {txType.type}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(tx.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <span className={`font-bold ${txType.color}`}>
                    {txType.sign}{tx.amount} ETH
                  </span>
                </div>

                <div className="text-sm text-gray-600 space-y-1">
                  <div>
                    <span className="font-medium">From:</span> {formatAddress(tx.sender_address)}
                  </div>
                  <div>
                    <span className="font-medium">To:</span> {formatAddress(tx.recipient_address)}
                  </div>
                  <div>
                    <span className="font-medium">Hash:</span>{' '}
                    <span className="font-mono text-xs">{formatAddress(tx.transaction_hash)}</span>
                  </div>
                  <div>
                    <span className="font-medium">Status:</span>{' '}
                    <span className={`capitalize ${tx.status === 'completed' ? 'text-green-600' : 'text-yellow-600'}`}>
                      {tx.status}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}