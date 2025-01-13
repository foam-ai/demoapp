import React from 'react';
import RequestQuoteForm from './RequestQuoteForm';
import { ProductData } from '../types';

interface QuoteRequestModalProps {
  product: ProductData;
  onClose: () => void;
}

const QuoteRequestModal: React.FC<QuoteRequestModalProps> = ({ product }) => {
  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex justify-center items-center z-50">
      <div className="relative bg-white p-6 rounded-lg shadow-lg w-11/12 md:w-1/2 lg:w-1/3">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-600 hover:text-gray-800 text-2xl"
        >
          &times;
        </button>
        <RequestQuoteForm productName={product.title}/>
      </div>
    </div>
  );
};

export default QuoteRequestModal;
