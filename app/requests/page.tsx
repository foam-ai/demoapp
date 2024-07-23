'use client';

import { useEffect, useState, FC } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { Request } from '@/app/types';

const Requests: FC = () => {
  const [requests, setRequests] = useState<Request[]>([]);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const fetchRequests = async () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    try {
      const response = await axios.get(`${backendUrl}/get_requests`);

      if (response.status === 200) {
        setRequests(response.data);
      } else {
        setFetchError('Failed to fetch requests');
      }
    } catch (error) {
      setFetchError('Something went wrong while fetching requests');
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const handleCreateQuotes = async (requestId: string, query: string) => {
    try {
      await axios.post(`https://garage-backend-kitd.onrender.com/create_quotes`, {
        query,
        request_id: requestId
      });
      fetchRequests();
    } catch (error) {
      console.error('Failed to create quotes', error);
    }
  };

  if (fetchError) return <div className="flex justify-center items-center h-screen text-red-500">{fetchError}</div>;

  return (
    <div className="container mx-auto px-4 py-8 text-black">
      <h1 className="text-3xl font-bold mb-4">Requests for Quotes</h1>
      <table className="min-w-full bg-white border border-gray-300 text-black">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">Request</th>
            <th className="py-2 px-4 border-b">Description</th>
            <th className="py-2 px-4 border-b">Status</th>
            <th className="py-2 px-4 border-b">Created At</th>
            <th className="py-2 px-4 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((request) => (
            <tr key={request.request_id} className="text-black">
              <td className="py-2 px-4 border-b">{request.product_name}</td>
              <td className="py-2 px-4 border-b">{request.description}</td>
              <td className="py-2 px-4 border-b">{request.status.toUpperCase()}</td>
              <td className="py-2 px-4 border-b">{new Date(request.created_at * 1000).toLocaleString()}</td>
              <td className="py-2 px-4 border-b">
                {request.status === 'COMPLETED' ? (
                  <Link className="text-blue-500 hover:underline" href={`/quotes/${request.request_id}`}>
                    See Quotes
                  </Link>
                ) : (
                  <button
                    onClick={() => handleCreateQuotes(request.request_id, request.product_name)}
                    className="text-blue-500 hover:underline"
                  >
                    Get Quotes
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Requests;
