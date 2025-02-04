'use client'

import Link from 'next/link'

export default function AuthError() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-red-600">Authentication Error</h1>
        <p className="mt-4 text-lg">There was a problem authenticating your account.</p>
        <div className="mt-8">
          <Link
            href="/login"
            className="rounded-md bg-black px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80"
          >
            Return to Login
          </Link>
        </div>
      </div>
    </div>
  )
} 