import React, { useState } from 'react';
import Image from 'next/image';

interface ImageGalleryProps {
  imageUrls: string[];
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ imageUrls }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [zoom, setZoom] = useState(false);

  const toggleZoom = () => setZoom(!zoom);

  return (
    <div className="flex">
      <div className="flex flex-col mr-4">
        {imageUrls.map((url, index) => (
          <div
            key={index}
            className={`cursor-pointer mb-2 border ${index === currentImageIndex ? 'border-blue-500' : 'border-gray-300'}`}
            onMouseEnter={() => setCurrentImageIndex(index)}
          >
            <Image
              src={url}
              alt={`Thumbnail ${index + 1}`}
              width={100}
              height={100}
              style={{ objectFit: 'cover' }}
              className="hover:opacity-75"
            />
          </div>
        ))}
      </div>
      <div className="relative w-full h-96 bg-white overflow-hidden cursor-zoom-in" onClick={toggleZoom}>
        <Image
          src={imageUrls[currentImageIndex]}
          alt="Product Image"
          fill
          style={{ objectFit: 'contain' }}
          className={`transition-transform duration-300 transform ${zoom ? 'scale-150' : ''}`}
        />
      </div>
    </div>
  );
};

export default ImageGallery;
