import React from 'react';
import { AlertCircle } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <div className="rounded-md bg-red-50 border border-red-200 p-4 mb-6">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <AlertCircle className="h-5 w-5 text-red-600" aria-hidden="true" />
        </div>
        <div className="ml-3 w-full">
          <h3 className="text-sm font-medium text-red-800">
            Payment Not Processed
          </h3>
          <div className="mt-2 text-sm text-red-700">
            <p className="leading-relaxed">
              {message || "We were unable to process your payment. Please verify payment information and try again."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
