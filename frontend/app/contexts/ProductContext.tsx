'use client';

import React, { createContext, useState, useContext, useEffect } from 'react';
import { getProductData } from '@/app/utils/getProductData';
import { ProductData } from '../types';

type ProductContextType = {
  applicationMap: Record<string, { title: string; url: string }[]>;
  productData: ProductData[];
};

const ProductContext = createContext<ProductContextType | undefined>(undefined);

export function ProductProvider({ children }: { children: React.ReactNode }) {
  const [applicationMap, setApplicationMap] = useState<Record<string, { title: string; url: string }[]>>({});
  const [productData, setProductData] = useState<ProductData[]>([]);

  useEffect(() => {
    const fetchProductData = async () => {
      const data = await getProductData();
      console.log('Fetched data:', data);
      setApplicationMap(data.applicationMap);
      setProductData(data.productData);
    };
    fetchProductData();
  }, []);

  return (
    <ProductContext.Provider value={{ applicationMap, productData }}>
      {children}
    </ProductContext.Provider>
  );
}

export function useProductContext() {
  const context = useContext(ProductContext);
  if (context === undefined) {
    throw new Error('useProductContext must be used within a ProductProvider');
  }
  return context;
}
