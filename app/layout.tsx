'use client';

import React, { useState } from 'react';
import { Inter } from 'next/font/google';
import { UserProvider } from '@auth0/nextjs-auth0/client';
import Header from '@/app/components/Header';
import Modal from '@/app/components/Modal';
import Footer from '@/app/components/Footer';
import ContactUs from '@/app/components/ContactUs';
import { ProductProvider, useProductContext } from '@/app/contexts/ProductContext';
import '@/app/styles/globals.css';
import '../app/styles/globals.css'

const inter = Inter({ subsets: ['latin'] });

function RootLayoutContent({ children }: { children: React.ReactNode }) {
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);
  const { applicationMap } = useProductContext();
  
  const openContactModal = () => setIsContactModalOpen(true);
  const closeContactModal = () => setIsContactModalOpen(false);

  return (
    <html lang="en" className={inter.className}>
      <head>
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
        <link
          rel="stylesheet"
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        />
      </head>
      <body>
        <UserProvider>
          <Header openContactModal={openContactModal} applicationMap={applicationMap} />
          <Modal isOpen={isContactModalOpen} onClose={closeContactModal}>
            <ContactUs onClose={closeContactModal} />
          </Modal>
          {children}
          <Footer />
        </UserProvider>
      </body>
    </html>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProductProvider>
      <RootLayoutContent>{children}</RootLayoutContent>
    </ProductProvider>
  );
}
