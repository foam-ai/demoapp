'use client'

import { useState } from 'react'
import CheckoutForm from '../components/CheckoutForm'
import ErrorMessage from '../components/ErrorMessage'
import Image from 'next/image'
import * as Sentry from '@sentry/node';

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
    try {
      const response = await fetch('https://demoapp-y43d.onrender.com/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cardnumber: formData.cardNumber,
          zipcode: formData.zipCode,
          firstName: formData.firstName,
          lastName: formData.lastName,
          street: formData.shippingStreet,
          city: formData.shippingCity,
          state: formData.shippingState,
          method: formData.shippingMethod
        }),
      })

      if (response.ok) {
        window.location.href = '/success'
      } else {
        const errorMessage = await response.json()
        setError('Sorry, something went wrong with your payment. Please try again.')
        Sentry.captureException(errorMessage)
      }
    } catch (error) {
      setError('Sorry, something went wrong with your payment. Please try again.')
      Sentry.captureException(error)
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
