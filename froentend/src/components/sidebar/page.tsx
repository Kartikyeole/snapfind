import React from 'react';
import { FaTachometerAlt, FaUser, FaCog, FaSignOutAlt } from 'react-icons/fa';

const Sidebar: React.FC = () => {
  return (
    <div className="inset-y-0 left-0 z-50 sidebar w-1/6 bg-gray-900 text-white h-[100vh] p-4 flex flex-col justify-between">
      <div>
        <h1 className="text-2xl font-bold mb-6">MyApp</h1>
        <ul>
          <li className="mb-4 flex items-center">
            <FaTachometerAlt className="mr-2" />
            <a href="/dashboard" className="hover:text-gray-400">Dashboard</a>
          </li>
          <li className="mb-4 flex items-center">
            <FaUser className="mr-2" />
            <a href="/profile" className="hover:text-gray-400">Profile</a>
          </li>
          <li className="mb-4 flex items-center">
            <FaCog className="mr-2" />
            <a href="/settings" className="hover:text-gray-400">Settings</a>
          </li>
        </ul>
      </div>
      <div>
        <ul>
          <li className="mb-4 flex items-center">
            <FaSignOutAlt className="mr-2" />
            <a href="/logout" className="hover:text-gray-400">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;