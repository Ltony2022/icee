import { useState, useEffect } from "react";
import { ChevronLeft } from "lucide-react";
import usePomodoro from "@/hooks/pomodoro";

const FocusApplet = () => {
  const { timer, mode } = usePomodoro();
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    let timeout: NodeJS.Timeout;
    if (isExpanded) {
      timeout = setTimeout(() => setIsExpanded(false), 3000);
    }
    return () => clearTimeout(timeout);
  }, [isExpanded]);

  return (
    <div className="fixed top-5 right-0 z-50">
      <div
        className={`
          relative transform transition-all duration-300 ease-out
          ${isExpanded ? "translate-x-0" : "translate-x-[calc(100%-22px)]"}
        `}
      >
        <div className="flex">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 bg-card border border-border/60 rounded-l-md hover:bg-secondary transition-colors"
          >
            <ChevronLeft
              className={`w-3.5 h-3.5 text-muted-foreground transition-transform duration-300 ${isExpanded ? "rotate-180" : ""}`}
            />
          </button>
          <div className="bg-card border border-l-0 border-border/60 rounded-r-md px-3 py-2 flex items-center gap-3">
            <p className="text-xs font-mono text-foreground/80">
              {Math.floor(timer / 60)}:{String(timer % 60).padStart(2, "0")}
            </p>
            <span className="text-[10px] font-mono text-muted-foreground/60 uppercase">
              {mode}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FocusApplet;
