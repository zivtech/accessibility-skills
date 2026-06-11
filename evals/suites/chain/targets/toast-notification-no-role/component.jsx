import React, { useState, useEffect } from 'react';

const BuggyToast = ({ message, duration = 3000 }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration]);

  if (!isVisible) {
    return null;
  }

  return (
    <div className="toast-notification">
      {/* Screen reader user may miss toast message entirely */}
      {message}
    </div>
  );
};

export default BuggyToast;
