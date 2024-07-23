"use client";
import React from 'react';
import { ProductData } from '../../app/types';
import ProductCard from './ProductCard'; // Import ProductCard component

interface InventoryProps {
  productData: ProductData[];
}

const Inventory: React.FC<InventoryProps> = ({ productData }) => {
  // Filter for Collaborative Robots
  const collaborativeRobots = productData.filter(product => product.category === 'collaborative-robot');

  // Randomly select products for "Products You May Like" and "Seen by Others"
  const shuffledProducts = productData.sort(() => 0.5 - Math.random());
  const productsYouMayLike = shuffledProducts.slice(0, 8); // Take first 5 as example
  const seenByOthers = shuffledProducts.slice(10, 20); // Take next 5 as example

  return (
    <div className="container mx-auto px-2 sm:px-10 py-4">
      <div>
        <h2 className="text-2xl font-bold my-4">Products You May Like</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {productsYouMayLike.map(product => (
            <ProductCard key={product.title} product={product} />
          ))}
        </div>
      </div>
      <div>
        <h2 className="text-2xl font-bold my-4">Collaborative Robots</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {collaborativeRobots.map(product => (
            <ProductCard key={product.title} product={product} />
          ))}
        </div>
      </div>
      <div>
        <h2 className="text-2xl font-bold my-4">Recently Seen by Others</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {seenByOthers.map(product => (
            <ProductCard key={product.title} product={product} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Inventory;
