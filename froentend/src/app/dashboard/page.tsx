
import React from 'react';
import Gallery from '@/components/Gallery';

const HomePage = () => {
  const images = [
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMohBeQLYtH8Xg4c94JUBDySkkUnoPR1G5Vg&s',
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-center mb-6">Dashboard Gallery</h1>
      <Gallery images={images} />
    </div>
  );
};

export default HomePage;