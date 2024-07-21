'use client';

import React, { useState, useCallback, ChangeEvent } from 'react';
import { FaSearch } from 'react-icons/fa';
import axios, { AxiosResponse } from 'axios';

type Item = {
  name: string;
  description: string;
  specs: { [key: string]: string | number | boolean };
};

const GenerativeInventory: React.FC = () => {
  const [filteredItems, setFilteredItems] = useState<Item[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const handleSearchButtonClick = useCallback(async () => {
    const query = searchTerm.toLowerCase().trim();
    if (query) {
      setLoading(true);
      setError(null);
      try {
        const response: AxiosResponse<{ content: { products: Item[] } }> = await axios.post(`${backendUrl}/api/openai`, {
          prompt: query
        });
        const items = response.data.content.products;
        setFilteredItems(Array.isArray(items) ? items : []);
      } catch (error) {
        setError("Failed to fetch items");
      } finally {
        setLoading(false);
      }
    }
  }, [searchTerm, backendUrl]);

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleSearchButtonClick();
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex mb-4 justify-center">
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={handleSearch}
          onKeyDown={handleKeyDown}
          className="w-full max-w-lg p-2 border rounded"
        />
        <button
          className="ml-2 p-2 border rounded bg-blue-500 text-white"
          onClick={handleSearchButtonClick}
        >
          <FaSearch />
        </button>
      </div>
      {loading ? (
        <div className="flex justify-center items-center min-h-screen">Loading...</div>
      ) : error ? (
        <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredItems.map((item, index) => (
            <div key={index} className="border p-4 rounded">
              <h2 className="font-bold mb-2 text-black">{item.name}</h2>
              <p className="mb-2 text-black">{item.description}</p>
              {Object.entries(item.specs).map(([key, value]) => (
                <div key={key}>
                  <strong>{key}:</strong> {String(value)}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenerativeInventory;
