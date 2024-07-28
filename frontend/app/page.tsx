'use client';

import { useProductContext } from './contexts/ProductContext';
import Inventory from './components/Inventory';

export default function Home() {
  const { productData } = useProductContext();

  return (
    <div className="container mx-auto p-4">
      <Inventory productData={productData} />
    </div>
  );
}
