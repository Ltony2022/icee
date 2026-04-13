import { flashcardSetProps } from "@/pages/ViewAllFlashcardSets";
import { useNavigate } from "react-router-dom";

interface FlashcardSetComponentProps extends flashcardSetProps {
  style?: React.CSSProperties;
}

const FlashcardSet = (displayData: FlashcardSetComponentProps) => {
  const navigate = useNavigate();

  return (
    <div
      className="group p-5 flex flex-col justify-between h-[140px] rounded-lg bg-card ring-1 ring-border/50 noise transition-all duration-200 hover:ring-copper/25 hover:bg-surface cursor-pointer animate-fade-up"
      style={displayData.style}
      onClick={() => {
        if (displayData.setId >= 0)
          navigate(`/flashcard/${displayData.setId}/manage`);
      }}
    >
      <div className="flex justify-between items-start">
        <h2 className="font-heading text-lg text-foreground/90 group-hover:text-copper transition-colors leading-tight pr-4">
          {displayData.name}
        </h2>
        <span className="text-[11px] font-mono text-muted-foreground/40 tabular-nums shrink-0">
          {displayData.numberOfCards}
        </span>
      </div>
      <div className="flex items-center justify-between">
        <span
          className={`text-[10px] font-mono font-medium uppercase tracking-wider ${
            displayData.needReview > 0
              ? "text-amber-400/80"
              : "text-sage/70"
          }`}
        >
          {displayData.needReview > 0
            ? `${displayData.needReview} to review`
            : "Caught up"}
        </span>
        <span className="text-[11px] font-mono text-muted-foreground/30 opacity-0 group-hover:opacity-100 group-hover:text-copper/60 transition-all duration-200">
          open &rarr;
        </span>
      </div>
    </div>
  );
};

export default FlashcardSet;
