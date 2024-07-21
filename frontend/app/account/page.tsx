'use client';

import '@/app/styles/globals.css';
import { useUser } from '@auth0/nextjs-auth0/client';
import { useEffect, useState, FC } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {User, UserLoaderProps} from '@/app/types';

const Account: FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/');
    }
  }, [isLoading, user, router]);


  return (
    <div>
      <UserLoader
        user={user}
        setUser={setUser}
        isLoading={isLoading}
        setIsLoading={setIsLoading}
        error={error}
        setError={setError}
      />
    </div>
  );
};

const UserLoader: FC<UserLoaderProps> = ({
  user,
  setUser,
  isLoading,
  setIsLoading,
  error,
  setError,
}) => {
  const { user: authUser, error: authError, isLoading: authIsLoading } = useUser();

  useEffect(() => {
    setUser(authUser as User);
    setIsLoading(authIsLoading);
    setError(authError ?? null);
  }, [authUser, authIsLoading, authError, setUser, setIsLoading, setError]);

  if (isLoading) return <div className="flex justify-center items-center h-screen">Loading...</div>;
  if (error) return <div className="flex justify-center items-center h-screen text-red-500">{error.message}</div>;

  return user ? (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4 text-black">Account</h1>
      <div className="flex items-center mb-6">
        <div className="text-center md:text-left">
          <h2 className="text-xl font-semibold text-black">Hello {user.name ?? 'User'}</h2>
          <p className="text-black">{user.email}</p>
        </div>
      </div>
      <button
        onClick={() => (window.location.href = '/api/auth/logout')}
        className="w-full md:w-auto bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition duration-300"
      >
        Logout
      </button>
    </div>
  ) : (
    <LoginButton />
  );
};

const LoginButton: FC = () => {
  return (
    <div className="flex justify-center items-center h-screen">
      <Link href="/api/auth/login">
        <a className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300">
          Login
        </a>
      </Link>
    </div>
  );
};

export default Account;
