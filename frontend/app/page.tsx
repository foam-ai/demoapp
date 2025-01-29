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
    let response;
    try {
      response = await fetch('https://demoapp-y43d.onrender.com/checkout', {
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
    } catch (error) {
      setError('We were unable to process your payment. Please verify payment information and try again.')
      throw new Error('Required to send shippingZipCode to checkout endpoint')
    }

      if (response?.ok) {
        window.location.href = '/success'
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
