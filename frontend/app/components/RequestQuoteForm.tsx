import React, { useState } from 'react';
import axios from 'axios';

interface RequestQuoteFormProps {
  productName: string;
  onClose?: () => void;
}

const RequestQuoteForm: React.FC<RequestQuoteFormProps> = ({ productName, onClose }) => {
  const [formData, setFormData] = useState({
    product_name: productName,
    condition: 'new',
    email: '',
    phone_number: '',
    name: '',
    company_name: '',
    message: '',
    zipcode: ''
  });
  console.log('Form data:', onClose);
  const [formError, setFormError] = useState('');
  const [formSuccess, setFormSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Don't submit if already submitting or if there's already a success message
    if (isSubmitting) return;
    
    setIsSubmitting(true);
    setFormError('');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    try {
      const dataToSubmit = {
        ...formData,
        created_at: Math.floor(Date.now() / 1000)
      };
      
      const response = await axios.post(`${backendUrl}/quotes`, dataToSubmit);
      
      if (response.status === 200) {
        setFormSuccess('Quote request submitted successfully!');
        // Reset form data after successful submission if needed
        // setFormData({...initialFormData});
      } else {
        setFormError('Failed to submit quote request');
      }
    } catch (error) {
      console.error('Submission error:', error);
      setFormError('An error occurred while submitting the quote request');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-gray-50 p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Request Quotes from 50 vendors in one click</h2>
      {formError && <p className="text-red-500 mb-4">{formError}</p>}
      {formSuccess && <p className="text-green-500 mb-4">{formSuccess}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="condition" className="block text-sm font-medium text-gray-700">Condition</label>
          <select
            id="condition"
            name="condition"
            value={formData.condition}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          >
            <option value="new">New</option>
            <option value="used">Used</option>
            <option value="both">Both</option>
          </select>
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700">Phone Number</label>
          <input
            id="phone_number"
            name="phone_number"
            type="tel"
            value={formData.phone_number}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
          <input
            id="name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <label htmlFor="company_name" className="block text-sm font-medium text-gray-700">Company Name</label>
          <input
            id="company_name"
            name="company_name"
            type="text"
            value={formData.company_name}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <label htmlFor="message" className="block text-sm font-medium text-gray-700">Message</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <label htmlFor="zipcode" className="block text-sm font-medium text-gray-700">Zip Code</label>
          <input
            id="zipcode"
            name="zipcode"
            type="text"
            value={formData.zipcode}
            onChange={handleInputChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <button
            type="submit"
            disabled={isSubmitting}
            className={`mt-4 w-full p-2 bg-yellow-300 text-black rounded hover:bg-yellow-200 ${
              isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            {isSubmitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default RequestQuoteForm;
