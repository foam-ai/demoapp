'use client'

import { useState } from 'react'
import CheckoutForm from '../components/CheckoutForm'
import ErrorMessage from '../components/ErrorMessage'
import Image from 'next/image'
import * as Sentry from '@sentry/nextjs'

export default function CheckoutPage() {
  const [error, setError] = useState<string>('')

  const handleCheckout = async (formData: {
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
  }) => {
      const response = await fetch('https://demoapp-y43d.onrender.com/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cardNumber: formData.cardNumber,
          zipCode: formData.zipCode,
          cvc: formData.cvc,
          firstName: formData.firstName,
          lastName: formData.lastName,
          shippingStreet: formData.shippingStreet,
          shippingCity: formData.shippingCity,
          shippingState: formData.shippingState,
          shippingMethod: formData.shippingMethod
        }),
      })

      if (response?.ok) {
        window.location.href = '/success'
      } else {
        const errorData = await response.json()
        
        // Create a custom error with additional context
        const error = new Error(errorData.message)
        error.name = 'CheckoutError'
        
        // Add extra context to Sentry
        Sentry.withScope(scope => {
          scope.setExtra('responseData', errorData)
          scope.setLevel('error')
          
          // Capture and throw the error
          Sentry.captureException(error)
          throw error
        })
      }
}

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8">
        <div className="text-center mb-8">
          <Image
            src="/tennis.png"
            alt="Tennis"
            width={300}
            height={300}
            className="mx-auto rounded-lg"
          />
        </div>
        {error && <ErrorMessage message={error} />}
        <CheckoutForm onSubmit={handleCheckout} />
      </div>
    </div>
  )
}
