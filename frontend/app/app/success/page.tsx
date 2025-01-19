// app/success/page.tsx
'use client'

export default function SuccessPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        
        <h1 className="text-3xl font-bold text-green-700 mb-2">
          Thank you for your order!
        </h1>
        
        <p className="text-gray-600 mb-8">
          We've received your order and will process it right away.
        </p>

        <div className="space-y-4">
          
          <button 
            onClick={() => window.location.href = '/'} 
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            ← Return to Shop
          </button>
        </div>
      </div>
    </div>
  )
}
