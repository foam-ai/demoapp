import React from 'react';
import { Check, ArrowLeft, Printer, Mail } from 'lucide-react';

const SuccessPage = () => {
  // Calculate delivery date (7 days from now)
  const deliveryDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white flex items-center justify-center p-4">
      <div className="max-w-lg w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center">
          {/* Static success checkmark */}
          <div className="mx-auto w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-6">
            <Check className="w-8 h-8 text-green-600" />
          </div>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-3">
            Order Confirmed!
          </h1>
          
          <p className="text-lg text-gray-600 mb-8">
            Thank you for your purchase. We&apos;ll send you a confirmation email shortly.
          </p>

          {/* Order details card */}
          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <div className="text-left space-y-4">
              <div>
                <p className="text-sm text-gray-500">Order Number</p>
                <p className="text-lg font-medium text-gray-900">
                  {'98238103'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Estimated Delivery</p>
                <p className="text-lg font-medium text-gray-900">{deliveryDate}</p>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button
                className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
              >
                <Printer className="w-4 h-4 mr-2" />
                Print Receipt
              </button>
              <button
                className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
              >
                <Mail className="w-4 h-4 mr-2" />
                View Order Details
              </button>
            </div>
            
            <button 
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-green-600 hover:text-green-500 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Return to Shop
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SuccessPage;
