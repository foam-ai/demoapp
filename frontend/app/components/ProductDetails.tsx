import React from 'react';
import { ProductData } from '../types';

interface ProductDetailsProps {
  product: ProductData;
  pdfUrl: string;
}

const ProductDetails: React.FC<ProductDetailsProps> = ({ product, pdfUrl }) => {
  return (
    <div className="p-4 bg-white rounded-lg">
      <p className="text-lg mb-6">{product.description}</p>
      <p className="text-lg font-semibold mb-2">
        Manufacturer: 
        <a href={product.url} target="_blank" className="text-gray-500 underline ml-1">
          {product.manufacturer}
        </a>
      </p>
      <div className="mt-6 flex">
        <div className="w-full">
          <h2 className="text-2xl font-bold mb-4">Specifications</h2>
          <table className="min-w-full bg-gray-50 border border-gray-300 rounded-lg">
            <thead>
              <tr>
                <th className="px-6 py-3 border-b border-gray-300 text-left text-xl font-bold text-gray-700">Specification</th>
                <th className="px-6 py-3 border-b border-gray-300 text-left text-xl font-bold text-gray-700">Details</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(product.specifications).map(([key, value]) => (
                <tr key={key}>
                  <td className="px-6 py-3 border-b border-gray-300 text-xl text-gray-700">{key}</td>
                  <td className="px-6 py-3 border-b border-gray-300 text-xl font-bold text-gray-700">{value as string}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="w-1/2 pl-4">
          <h2 className="text-2xl font-bold mb-4">Applications</h2>
          <ul className="list-disc ml-6 text-lg">
            {Object.entries(product.applications).map(([name, link]) => (
              <li key={name}>
                <a href={link} target="_blank" className="text-gray-500 underline">
                  {name}
                </a>
              </li>
            ))}
          </ul>
          <a href={pdfUrl} target="_blank" className="text-lg font-bold text-gray-500 underline mt-4 block">View Full Specifications</a>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
