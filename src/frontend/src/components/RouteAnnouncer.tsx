import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

/**
 * Announces route changes to screen readers via an aria-live region.
 * Renders a visually hidden element that updates on every location change.
 */
export default function RouteAnnouncer() {
  const location = useLocation();
  const [announcement, setAnnouncement] = useState("");

  useEffect(() => {
    // Small delay to let the new page render its <h1>
    const timer = setTimeout(() => {
      const h1 = document.querySelector("h1");
      const title = h1?.textContent || document.title;
      setAnnouncement(title);
    }, 100);
    return () => clearTimeout(timer);
  }, [location.pathname]);

  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      role="status"
      className="sr-only"
    >
      {announcement}
    </div>
  );
}
