interface ErrorMessageProps {
    message: string
  }
  
  export default function ErrorMessage({ message }: ErrorMessageProps) {
    return (
      <div className="rounded-md bg-red-50 p-4 mb-6">
        <div className="flex">
          <div className="ml-3">
            <div className="mt-2 text-md text-center text-red-700">
              {message}
            </div>
          </div>
        </div>
      </div>
    )
  }
