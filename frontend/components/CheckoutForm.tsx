'use client'

import { useState } from 'react'
import { Lock, Truck } from 'lucide-react'

interface CheckoutFormProps {
  onSubmit: (formData: {
    firstName: string
    lastName: string
    cardNumber: string
    cvc: string
    zipCode: string
    shippingStreet: string
    shippingCity: string
    shippingState: string
    shippingZipCode: string
    shippingMethod: string
  }) => Promise<void>
}

export default function CheckoutForm({ onSubmit }: CheckoutFormProps) {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [cardNumber, setCardNumber] = useState('')
  const [cvc, setCvc] = useState('')
  const [zipCode, setZipCode] = useState('')
  const [shippingStreet, setShippingStreet] = useState('')
  const [shippingCity, setShippingCity] = useState('')
  const [shippingState, setShippingState] = useState('')
  const [shippingZipCode, setShippingZipCode] = useState('')
  const [shippingMethod, setShippingMethod] = useState('standard')
  const [isLoading, setIsLoading] = useState(false)


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await onSubmit({
        firstName,
        lastName,
        cardNumber,
        cvc,
        zipCode,
        shippingStreet,
        shippingCity,
        shippingState,
        shippingZipCode,
        shippingMethod
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="firstName" className="block text-sm font-medium text-gray-500">
              First Name
            </label>
            <input
              type="text"
              id="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
              required
            />
          </div>
          
          <div>
            <label htmlFor="lastName" className="block text-sm font-medium text-gray-500">
              Last Name
            </label>
            <input
              type="text"
              id="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
              required
            />
          </div>
        </div>

        <div className="space-y-4">
  <h3 className="text-md font-medium text-gray-700">Shipping Address</h3>
  
  <div className="space-y-4">
    <div>
      <label htmlFor="shippingStreet" className="block text-sm font-medium text-gray-500">Street Address</label>
      <input
        type="text"
        id="shippingStreet"
        value={shippingStreet}
        onChange={(e) => setShippingStreet(e.target.value)}
        className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
        required
      />
    </div>

    <div className="grid grid-cols-12 gap-4">
      <div className="col-span-6">
        <label htmlFor="shippingCity" className="block text-sm font-medium text-gray-500">City</label>
        <input
          type="text"
          id="shippingCity"
          value={shippingCity}
          onChange={(e) => setShippingCity(e.target.value)}
          className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
          required
        />
      </div>
      <div className="col-span-3">
        <label htmlFor="shippingState" className="block text-sm font-medium text-gray-500">State</label>
        <input
          type="text"
          id="shippingState"
          value={shippingState}
          onChange={(e) => setShippingState(e.target.value)}
          className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
          required
        />
      </div>
      <div className="col-span-3">
        <label htmlFor="shippingZipCode" className="block text-sm font-medium text-gray-500">ZIP Code</label>
        <input
          type="text"
          id="shippingZipCode"
          value={shippingZipCode}
          onChange={(e) => setShippingZipCode(e.target.value)}
          className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
          required
        />
      </div>
    </div>
  </div>
</div>

        <div>
          <div className="block text-sm font-medium text-gray-700 mb-2">
            Shipping Method
          </div>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <input
                type="radio"
                id="shipping-standard"
                name="shippingMethod"
                value="standard"
                checked={shippingMethod === 'standard'}
                onChange={(e) => setShippingMethod(e.target.value)}
                className="h-4 w-4 border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="shipping-standard" className="flex items-center gap-2 cursor-pointer">
                <Truck className="w-5 h-5 text-blue-600" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Standard Shipping</p>
                  <p className="text-sm text-gray-500">5-7 business days</p>
                </div>
              </label>
            </div>
            
            <div className="flex items-center gap-3">
              <input
                type="radio"
                id="shipping-express"
                name="shippingMethod"
                value="express"
                checked={shippingMethod === 'express'}
                onChange={(e) => setShippingMethod(e.target.value)}
                className="h-4 w-4 border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="shipping-express" className="flex items-center gap-2 cursor-pointer">
                <Truck className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Express Shipping</p>
                  <p className="text-sm text-gray-500">2-3 business days</p>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div className="space-y-4">
  <h3 className="text-md font-medium text-gray-700">Payment Information</h3>
  
  <div className="space-y-4">
    <div>
      <label htmlFor="cardNumber" className="block text-sm font-medium text-gray-500">
        Card Number
      </label>
      <input
        type="text"
        id="cardNumber"
        value={cardNumber}
        onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))}
        maxLength={16}
        className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
        required
      />
    </div>

    <div className="grid grid-cols-12 gap-4">
      <div className="col-span-6">
        <label htmlFor="cvc" className="block text-sm font-medium text-gray-500">
          CVC
        </label>
        <input
          type="text"
          id="cvc"
          value={cvc}
          onChange={(e) => setCvc(e.target.value.replace(/\D/g, ''))}
          maxLength={4}
          className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
          required
        />
      </div>

      <div className="col-span-6">
        <label htmlFor="zipCode" className="block text-sm font-medium text-gray-500">
          ZIP Code
        </label>
        <input
          type="text"
          id="zipCode"
          value={zipCode}
          onChange={(e) => setZipCode(e.target.value.replace(/\D/g, ''))}
          maxLength={5}
          className="text-sm mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
          required
        />
      </div>
    </div>
  </div>
</div>
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Lock className="w-4 h-4" />
            <span>Secure payment</span>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
        >
          {isLoading ? 'Processing...' : 'Place Order'}
        </button>
      </form>
    </div>
  )
}
