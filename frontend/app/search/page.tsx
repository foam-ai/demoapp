'use client';

import { Suspense } from 'react';
import { useProductContext } from '../contexts/ProductContext';
import Search from '@/app/components/Search';

export default function SearchPage() {
  const { productData } = useProductContext();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Search productData={productData} />
    </Suspense>
  );
}