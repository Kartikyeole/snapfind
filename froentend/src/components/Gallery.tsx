import React from 'react';
import Image from 'next/image';

interface GalleryProps {
  images: string[];
}

const Gallery: React.FC<GalleryProps> = ({ images }) => {
  return (
    <div>
      {images.map((image, index) => (
        <Image
          key={index}
          src={image}
          alt="Gallery image"
          width={600}
          height={400}
          objectFit="cover"
          className="rounded-lg"
        />
        )
      )
        }
      
    </div>
  );
};

export default Gallery;