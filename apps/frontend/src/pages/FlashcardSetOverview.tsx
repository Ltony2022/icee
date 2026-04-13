import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { FaArrowLeft, FaPen, FaCog } from "react-icons/fa";

interface setMetadata {
  setName: string;
  totalFlashcards: number;
  needReview: number;
}

const ManageFlashcard = () => {
  const [setMetadata, setSetMetadata] = useState<setMetadata>({
    setName: "",
    totalFlashcards: 0,
    needReview: 0,
  });
  const { setId } = useParams();
  const navigate = useNavigate();

  const getMetadata = useCallback(async () => {
    const response = await axios.get(
      `${getBackendOrigin()}/flashcards/set/${setId}/info`
    );
    setSetMetadata(response.data);
  }, [setId]);

  useEffect(() => {
    getMetadata();
  }, [getMetadata]);

  const reviewPercent =
    setMetadata.totalFlashcards > 0
      ? Math.round(
          ((setMetadata.totalFlashcards - setMetadata.needReview) /
            setMetadata.totalFlashcards) *
            100
        )
      : 100;

  return (
    <div className="mx-auto w-full max-w-2xl px-8 py-12">
      {/* Back */}
      <button
        onClick={() => navigate("/user-flashcards")}
        className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground/80 transition-colors mb-10 group animate-fade-up"
      >
        <FaArrowLeft
          size={10}
          className="group-hover:-translate-x-0.5 transition-transform"
        />
        <span className="font-mono text-xs">All sets</span>
      </button>

      {/* Title */}
      <div className="mb-12 animate-fade-up" style={{ animationDelay: "60ms" }}>
        <h1 className="font-heading text-4xl text-foreground/95 tracking-tight leading-tight">
          {setMetadata.setName || (
            <span className="text-muted-foreground/40">Loading...</span>
          )}
        </h1>
        <p className="text-muted-foreground text-sm mt-2 font-mono">
          {setMetadata.totalFlashcards} card
          {setMetadata.totalFlashcards !== 1 ? "s" : ""} in this set
        </p>
      </div>

      {/* Stats */}
      <div
        className="grid grid-cols-2 gap-3 mb-10 animate-fade-up"
        style={{ animationDelay: "120ms" }}
      >
        <div className="rounded-lg bg-card ring-1 ring-border/50 p-5 noise">
          <p className="text-[10px] font-mono text-muted-foreground/50 uppercase tracking-wider mb-2">
            Need Review
          </p>
          <p className="font-heading text-4xl text-amber-400/90 tracking-tight">
            {setMetadata.needReview}
          </p>
        </div>
        <div className="rounded-lg bg-card ring-1 ring-border/50 p-5 noise">
          <p className="text-[10px] font-mono text-muted-foreground/50 uppercase tracking-wider mb-2">
            Mastery
          </p>
          <p className="font-heading text-4xl text-sage/90 tracking-tight">
            {reviewPercent}
            <span className="text-base font-sans text-muted-foreground/30 ml-0.5">
              %
            </span>
          </p>
        </div>
      </div>

      {/* CTA */}
      <div
        className="mb-14 animate-fade-up"
        style={{ animationDelay: "180ms" }}
      >
        {setMetadata.needReview > 0 ? (
          <button
            onClick={() => navigate(`/flashcard/${setId}/learn`)}
            className="w-full py-4 rounded-lg bg-copper text-copper-foreground font-medium text-[15px] transition-all hover:brightness-110 shadow-lg shadow-copper/10"
          >
            Start Learning Session
          </button>
        ) : (
          <div className="w-full py-4 rounded-lg bg-sage/10 ring-1 ring-sage/20 text-center text-sage text-sm font-medium">
            All caught up — no cards need review.
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="animate-fade-up" style={{ animationDelay: "240ms" }}>
        <p className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-4 ml-1">
          Manage
        </p>
        <div className="flex flex-col gap-1">
          <button
            onClick={() => navigate(`/flashcard/${setId}/manageFlashcardSet`)}
            className="group w-full flex items-center justify-between px-4 py-3.5 rounded-lg hover:bg-secondary/60 transition-all text-left"
          >
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-md bg-copper/10 ring-1 ring-copper/15 flex items-center justify-center text-copper/70 group-hover:text-copper transition-colors">
                <FaPen size={11} />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/80">
                  Edit Cards
                </p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Add, edit, or remove flashcards
                </p>
              </div>
            </div>
            <span className="text-xs font-mono text-muted-foreground/30 group-hover:text-copper/60 transition-all opacity-0 group-hover:opacity-100">
              open
            </span>
          </button>

          <div className="w-full flex items-center justify-between px-4 py-3.5 rounded-lg opacity-40 cursor-not-allowed text-left">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-md bg-muted ring-1 ring-border/60 flex items-center justify-center text-muted-foreground/40">
                <FaCog size={11} />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/80">
                  Settings
                </p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Spaced repetition & visibility
                </p>
              </div>
            </div>
            <span className="text-[9px] font-mono text-muted-foreground/40 bg-muted px-1.5 py-0.5 rounded">
              soon
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManageFlashcard;
