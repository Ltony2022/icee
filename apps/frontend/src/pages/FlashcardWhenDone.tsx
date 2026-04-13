import useFlashcardPerformanceTracker from "@/hooks/trackUserPerformance";
import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const FlashcardWhenDone = () => {
  const {
    totalFlashcards,
    totalReviewed,
    totalSkipped,
    calculateSkipped,
    resetPerformance,
  } = useFlashcardPerformanceTracker();
  const navigate = useNavigate();
  const { setId } = useParams();

  useEffect(() => {
    calculateSkipped();
  }, [calculateSkipped]);

  const stats = [
    { label: "Total Cards", value: totalFlashcards },
    { label: "Answered", value: totalReviewed },
    { label: "Skipped", value: totalSkipped },
  ];

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm z-50 animate-fade-in">
      <div className="w-full max-w-sm rounded-lg bg-card ring-1 ring-border/60 p-8 noise animate-fade-up">
        <div className="text-center mb-8">
          <h1 className="font-heading text-3xl text-foreground/95 mb-1">
            Session <span className="italic text-copper">Complete</span>
          </h1>
          <p className="text-sm text-muted-foreground">
            Great work on this study session.
          </p>
        </div>

        <div className="space-y-2 mb-8">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="flex items-center justify-between px-4 py-2.5 rounded-md bg-background/80"
            >
              <span className="text-sm text-muted-foreground">
                {stat.label}
              </span>
              <span className="text-sm font-mono font-medium text-foreground/80 tabular-nums">
                {stat.value}
              </span>
            </div>
          ))}
        </div>

        <div className="flex gap-2.5">
          <button
            onClick={() => navigate("/")}
            className="flex-1 py-2.5 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground/80 hover:bg-secondary/60 transition-colors ring-1 ring-border/40"
          >
            Home
          </button>
          {totalSkipped > 0 && (
            <button
              className="flex-1 py-2.5 rounded-md text-sm font-medium bg-copper text-copper-foreground hover:brightness-110 transition-all shadow-sm shadow-copper/10"
              onClick={() => {
                resetPerformance();
                navigate(`/flashcard/${setId}/learn`);
              }}
            >
              Review Skipped
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default FlashcardWhenDone;
