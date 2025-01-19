'use client'
import { useState } from 'react'
import CheckoutForm from '../components/CheckoutForm'
import ErrorMessage from '../components/ErrorMessage'
import Image from 'next/image'

export default function CheckoutPage() {
  const [error, setError] = useState<string>('')

  const handleCheckout = async (cardNumber: string, zipCode: string) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cardnumber: cardNumber, zipcode: zipCode }),
      })

      if (response.ok) {
        window.location.href = '/success'
      } else {
        setError('Sorry, something went wrong with your payment. Please try again.')
      }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <div className="text-center mb-8">
          <Image
            src="/hat.png"
            alt="Hat"
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
