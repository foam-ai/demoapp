import React from 'react';
import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-gray-500 text-white p-4 mt-8">
      <div className="container mx-auto flex justify-between items-center">
        <div>
          <h3 className="font-bold text-lg">Demo Store, Inc</h3>
          <p>4529 Oak Avenue, Portland, OR 97205</p>
        </div>
        <div>
          <Link href="/contact-us">
            <div className="px-4 text-white hover:underline hover:text-white">Contact Us</div>
          </Link>
          <Link href="/terms">
            <div className="px-4 text-white hover:underline hover:text-white">Terms and Conditions</div>
          </Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
