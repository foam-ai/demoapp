import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ProductData } from '../types';
import QuoteRequestModal from './QuoteRequestModal';

interface ProductCardProps {
  product: ProductData;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [showModal, setShowModal] = useState(false);
  const imageUrl = `/data/${product.category}/${product.directory}/image0.png`;

  const handleGetQuoteClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setShowModal(true);
  };

  return (
    <div className="flex flex-col justify-between p-4 border rounded shadow-md group no-underline text-black h-full w-full">
        <Link href={`/products/${product.category}/${product.directory}`} className="hover:no-underline">
        <div>
            <h1 className="text-2xl font-bold mb-4 text-black hover:no-underline">{product.title}</h1>
            <div className="relative h-48 w-full bg-white mb-4">
            <Image
              src={imageUrl}
              alt="Product Image"
              fill
              style={{ objectFit: 'contain' }} 
              className="transition-transform duration-300 transform group-hover:scale-110"
            />
          </div>
        </div>
      </Link>
      <div className="mt-auto flex justify-center">
        <button
          onClick={handleGetQuoteClick}
          className="py-2 px-4 bg-yellow-300 text-black rounded hover:bg-yellow-200 text-base"
        >
          Get Quotes
        </button>
      </div>
      {showModal && (
        <QuoteRequestModal product={product} onClose={() => setShowModal(false)} />
      )}
    </div>
  );
};

export default ProductCard;
