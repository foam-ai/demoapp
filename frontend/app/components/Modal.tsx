import { FC } from 'react';
import { ModalProps } from '../types';

const Modal: FC<ModalProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
      <div className="relative bg-white p-6 rounded shadow-lg">
        <button onClick={onClose} className="absolute top-0 right-0 m-4 text-gray-500 hover:text-gray-700">
          ×
        </button>
        {children}
      </div>
    </div>
  );
};

export default Modal;
