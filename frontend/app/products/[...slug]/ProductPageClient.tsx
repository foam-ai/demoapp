'use client';

import React from 'react';
import ImageGallery from '../../components/ImageGallery';
import ProductDetails from '../../components/ProductDetails';
import RequestQuoteForm from '../../components/RequestQuoteForm';
import { ProductData } from '../../types';

interface ProductPageClientProps {
  product: ProductData;
  imageUrls: string[];
  pdfUrl: string;
}

const ProductPageClient: React.FC<ProductPageClientProps> = ({ product, imageUrls, pdfUrl }) => {
  return (
    <div className="container mx-auto p-4 text-black flex">
      <div className="w-2/3 pr-8">
        <h1 className="text-3xl font-bold mb-6">{product.title}</h1>
        <ImageGallery imageUrls={imageUrls} />
        <ProductDetails product={product} pdfUrl={pdfUrl} />
      </div>
      <div className="flex justify-center items-start">
        <div className="w-full max-w-lg">
          <RequestQuoteForm productName={product.title} />
        </div>
      </div>
    </div>
  );
};

export default ProductPageClient;
