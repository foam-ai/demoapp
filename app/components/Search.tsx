'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { ProductData } from '@/app/types';
import ProductCard from '@/app/components/ProductCard';

interface SearchProps {
  productData: ProductData[];
}

export default function Search({ productData }: SearchProps) {
  const searchParams = useSearchParams();
  const [term, setTerm] = useState<string | null>(null);

  useEffect(() => {
    const searchTerm = searchParams?.get('term') ?? null;
    setTerm(searchTerm);
  }, [searchParams]);

  const filteredProducts = term
    ? productData.filter(product =>
        product.title.toLowerCase().includes(term.toLowerCase())
      )
    : productData;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">
        {term ? `Search results for "${term}"` : 'All Products'}
      </h1>
      {filteredProducts.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredProducts.map((product) => (
            <ProductCard key={product.title} product={product} />
          ))}
        </div>
      ) : (
        <p>No products found.</p>
      )}
    </div>
  );
}