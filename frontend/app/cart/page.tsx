'use client';

import React, { useState, useEffect } from 'react';
import { Quote } from '@/app/types';

const Cart = () => {
  const [cart, setCart] = useState<Quote[]>([]);

  useEffect(() => {
    const loadedCart = JSON.parse(localStorage.getItem('cart') || '[]');
    setCart(loadedCart);
  }, []);

  const handleRemoveItem = (index: number) => {
    const updatedCart = cart.filter((_, idx) => idx !== index);
    setCart(updatedCart);
    localStorage.setItem('cart', JSON.stringify(updatedCart));
  };

  if (cart.length === 0) {
    return <div className='container mx-auto p-4 text-black'>Your cart is empty.</div>;
  }

  return (
    <div className='container mx-auto p-4'>
      <h1 className='text-3xl font-bold text-black'>Shopping Cart</h1>
      <div className='my-4'>
        {cart.map((item, index) => (
          <div key={index} className='flex justify-between items-center p-4 border-b'>
            <div>
              <h2 className='text-xl font-bold text-black'>{item.title}</h2>
              <p className='text-black'>${item.price}</p>
              <p className='text-black'>Supplier: {item.source}</p>
            </div>
            <div>
              <button
                onClick={() => handleRemoveItem(index)}
                className='bg-red-500 hover:bg-red-700 text-black font-bold py-2 px-4 rounded'
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>
      <button className='bg-green-500 hover:bg-green-700 text-black font-bold py-2 px-4 rounded float-right'>Checkout Now</button>
    </div>
  );
};

export default Cart;
