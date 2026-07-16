import { useState } from "react";

/**
 * Save button + persistent live region (the robust announcement pattern:
 * region mounted empty, text injected on action) — plus a deliberately
 * naive toast (mounts WITH content) to check calibration rule 3 in Storybook.
 */
export const ToastStatus = ({ naive = false }) => {
  const [statusText, setStatusText] = useState("");
  const [naiveToastVisible, setNaiveToastVisible] = useState(false);

  const handleSave = () => {
    if (naive) {
      setNaiveToastVisible(true);
    } else {
      setStatusText("Item saved");
    }
  };

  return (
    <main>
      <h2>Order editor</h2>
      <p>$29.00</p>
      <button onClick={handleSave}>Save order</button>
      {!naive && <div role="status" data-testid="app-status">{statusText}</div>}
      {naive && naiveToastVisible && (
        <div role="alert" className="toast">Item saved</div>
      )}
    </main>
  );
};
