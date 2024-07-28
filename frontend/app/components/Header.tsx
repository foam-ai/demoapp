'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import '@/app/styles/globals.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faEnvelope } from '@fortawesome/free-solid-svg-icons';

const Header = ({
  openContactModal,
  applicationMap = {},
}: {
  openContactModal: () => void;
  applicationMap: Record<string, { title: string; url: string }[]>;
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const router = useRouter();
  const [topApplications, setTopApplications] = useState<string[]>([]);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

  useEffect(() => {
    console.log('applicationMap:', applicationMap);
    const topApps = Object.keys(applicationMap).slice(0, 6);
    setTopApplications(topApps);
    console.log('topApplications:', topApps);
  }, [applicationMap]);

  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    router.push(`/search?term=${searchTerm}`);
  };

  return (
    <header className="flex flex-col items-center p-4 bg-blue-400 custom-header-height">
      <div className="flex justify-between items-center w-full mb-2">
        <div className="text-5xl font-bold text-gray-800">
          <Link href="/" className="no-underline text-black hover:text-gray-800 focus:text-gray-800 visited:text-gray-800 hover:no-underline">
            DEMO STORE
          </Link>
        </div>
        <form onSubmit={handleSearch} className="flex w-full max-w-5xl mx-6">
          <input
            type="text"
            placeholder="Search products..."
            className="flex-grow p-2 border border-gray-300 rounded-l text-black"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button
            type="submit"
            className="p-2 bg-yellow-500 text-white rounded-r hover:bg-yellow-500"
          >
            <FontAwesomeIcon icon={faSearch} />
          </button>
        </form>
        <div className="flex space-x-4">
          <button onClick={openContactModal} className="flex items-center text-black hover:text-gray-600">
            <FontAwesomeIcon icon={faEnvelope} className="mr-2" />
            Contact Us
          </button>
        </div>
      </div>
      <div className="text-4xl font-bold text-black mt-2 mb-2">
        SHOP ALL OF YOUR ROBOTS WITH ONE CLICK
      </div>
      <nav className="flex space-x-4">
        {topApplications.map((application) => (
          <div
            key={application}
            className="relative group"
            onMouseEnter={() => setActiveDropdown(application)}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <button className="text-lg text-gray-800 hover:text-gray-800 pb-2 group-hover:text-gray-800">
              {application}
            </button>
            {activeDropdown === application && (
              <div className="absolute left-0 z-50" style={{ zIndex: 9999 }}>
                <div className="pt-2">
                  <div className="bg-white shadow-lg rounded py-2">
                    <ul className={`
                      ${applicationMap[application]?.length > 10 ? 'max-h-96 overflow-y-auto' : ''}
                      scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200
                      hover:scrollbar-thumb-gray-500
                    `}>
                      {applicationMap[application]?.map((product) => (
                        <li key={product.title}>
                          <Link
                            href={product.url}
                            className="block px-4 py-2 text-gray-800 hover:bg-gray-300 hover:text-gray-800 hover:no-underline whitespace-nowrap"
                          >
                            {product.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </nav>
    </header>
  );
};

export default Header;
