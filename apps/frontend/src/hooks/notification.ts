import { useCallback, useState } from "react";

export type NotificationType = "success" | "error" | "warning" | "info";

export interface NotificationProps {
  type?: NotificationType;
  message: string;
  isVisible: boolean;
  onClose: () => void;
  duration?: number;
}

export const useNotification = () => {
  const [notification, setNotification] = useState<NotificationProps>({
    type: "info",
    message: "",
    isVisible: false,
    onClose: () => closeNotification(),
  });

  // set the notification message and type
  const notify = useCallback((message: string, type: NotificationType) => {
    setNotification((old) => ({
      ...old,
      message,
      type,
      isVisible: true,
    }));
  }, []);

  // clear the notification
  const closeNotification = useCallback(() => {
    setNotification((old) => ({
      ...old,
      message: "",
      isVisible: false,
    }));
  }, []);

  return {
    notification,
    notify,
    closeNotification,
  };
};
