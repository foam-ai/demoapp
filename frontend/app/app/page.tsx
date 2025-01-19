'use client'
import { useState } from 'react'
import CheckoutForm from '../components/CheckoutForm'
import ErrorMessage from '../components/ErrorMessage'
import Image from 'next/image'

export default function CheckoutPage() {
  const [error, setError] = useState<string>('')

  const handleCheckout = async (cardNumber: string, zipCode: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cardNumber, zipCode }),
      })

      if (response.ok) {
        window.location.href = '/success'
      } else {
        const data = await response.json()
        setError(data.message || 'An error occurred during checkout')
      }
    } catch (err) {
      setError('Failed to process checkout')
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
