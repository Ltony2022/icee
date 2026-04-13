import { NotificationProps } from "@/hooks/notification";
import { AnimatePresence, motion } from "framer-motion";
import React from "react";
import {
  IoCheckmarkCircle,
  IoCloseCircle,
  IoInformationCircle,
  IoWarning,
} from "react-icons/io5";

// export type NotificationType = 'success' | 'error' | 'warning' | 'info';

// interface NotificationProps {
//   type?: NotificationType;
//   message: string;
//   isVisible: boolean;
//   onClose: () => void;
//   duration?: number;
// }

const iconMap = {
  success: <IoCheckmarkCircle className="w-6 h-6 text-green-500" />,
  error: <IoCloseCircle className="w-6 h-6 text-red-500" />,
  warning: <IoWarning className="w-6 h-6 text-yellow-500" />,
  info: <IoInformationCircle className="w-6 h-6 text-blue-500" />,
};

const bgColorMap = {
  success: "bg-green-50",
  error: "bg-red-50",
  warning: "bg-yellow-50",
  info: "bg-blue-50",
};

export const ToastNotification: React.FC<NotificationProps> = ({
  type = "info",
  message,
  isVisible,
  onClose,
  duration = 3000,
}) => {
  React.useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [isVisible, duration, onClose]);

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          className={`fixed top-4 right-4 z-50 flex items-center p-4 rounded-lg shadow-lg ${bgColorMap[type]}`}
        >
          <div className="flex items-center space-x-3">
            {iconMap[type]}
            <p className="text-gray-700">{message}</p>
          </div>
          <button
            onClick={onClose}
            className="ml-4 text-gray-400 hover:text-gray-600 focus:outline-none"
          >
            <IoCloseCircle className="w-5 h-5" />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
