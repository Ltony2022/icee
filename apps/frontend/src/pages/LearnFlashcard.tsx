import { ToastNotification } from "@/components/common/notification";
import FlashCard from "@/components/flashcards/FlashCard";
import { useNotification } from "@/hooks/notification";
import useFlashcardPerformanceTracker from "@/hooks/trackUserPerformance";
import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";

export interface FlashCardType {
  flashcard_id: number;
  question: string;
  answer: string;
}

function DifficultyButtons({
  isAnswer,
  fcid,
  onSkip,
  userAnswered,
}: {
  isAnswer: boolean;
  fcid: number;
  onSkip: () => void;
  userAnswered: (fcid: number, difficulty: string) => void;
}) {
  if (!isAnswer) {
    return (
      <div className="mt-8 flex justify-center w-full max-w-xl animate-fade-up">
        <button
          className="rounded-md px-6 py-2.5 text-[13px] font-medium text-muted-foreground hover:text-foreground/70 hover:bg-secondary/60 transition-all w-full ring-1 ring-border/40"
          onClick={onSkip}
        >
          Skip Question
        </button>
      </div>
    );
  }

  return (
    <div className="mt-8 flex flex-col items-center w-full max-w-xl animate-fade-up">
      <p className="mb-4 text-[10px] font-mono text-muted-foreground/40 uppercase tracking-[0.15em]">
        How easily did you answer this?
      </p>
      <div className="flex items-center gap-2 w-full">
        <button
          className="flex-1 rounded-md py-2.5 bg-sage/10 text-sage hover:bg-sage/20 transition-colors text-sm font-medium ring-1 ring-sage/15"
          onClick={() => userAnswered(fcid, "easy")}
        >
          Easy
        </button>
        <button
          className="flex-1 rounded-md py-2.5 bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 transition-colors text-sm font-medium ring-1 ring-amber-500/15"
          onClick={() => userAnswered(fcid, "medium")}
        >
          Medium
        </button>
        <button
          className="flex-1 rounded-md py-2.5 bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 transition-colors text-sm font-medium ring-1 ring-rose-500/15"
          onClick={() => userAnswered(fcid, "hard")}
        >
          Hard
        </button>
        <button
          className="rounded-md py-2.5 px-4 text-muted-foreground/60 hover:text-foreground/60 hover:bg-secondary/60 transition-colors text-sm font-medium ring-1 ring-border/30"
          onClick={onSkip}
        >
          Skip
        </button>
      </div>
    </div>
  );
}

export default function FlashCardPage() {
  const { setId } = useParams();
  const [isAnswer, setIsAnswer] = useState(false);

  const { notification, closeNotification, notify } = useNotification();
  const { setTotalFlashcards, addReviewed } = useFlashcardPerformanceTracker();

  const [currentFlashCard, setCurrentFlashCard] = useState<number>(0);
  const [flashCardData, setFlashCardData] = useState<FlashCardType[]>([]);
  const [setMetadata, setSetMetadata] = useState<{
    setName?: string;
    needReview?: number;
  }>({});
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(`${getBackendOrigin()}/flashcards/set/${setId}/info`)
      .then((response) => {
        setSetMetadata(response.data);
        setTotalFlashcards(response.data.needReview || 0);
      })
      .catch(console.error);
  }, [setId, setTotalFlashcards]);

  function nextFlashCard() {
    if (currentFlashCard + 1 >= flashCardData.length) {
      navigate(`/flashcard/${setId}/done`);
      return;
    }
    setCurrentFlashCard((prev) => prev + 1);
    setIsAnswer(false);
  }

  function userAnswered(fcid: number, difficulty: string) {
    let difficultyValue = 0;
    if (difficulty === "easy") difficultyValue = 5;
    else if (difficulty === "medium") difficultyValue = 3;
    else if (difficulty === "hard") difficultyValue = 1;

    axios
      .put(
        `${getBackendOrigin()}/flashcards/set/${setId}/updateUserFlashcard`,
        JSON.stringify({ flashcard_id: fcid, user_grade: difficultyValue }),
        { headers: { "Content-Type": "application/json" } }
      )
      .then(() => {
        addReviewed();
        nextFlashCard();
      })
      .catch(() => notify("Failed to update flashcard", "error"));
  }

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(
        `${getBackendOrigin()}/flashcards/set/${setId}/getPracticeFlashcard`
      );
      setFlashCardData(response.data);
    }
    fetchData();
  }, [setId]);

  const data = flashCardData;

  return (
    <div className="mx-auto w-full max-w-3xl px-6 py-10 flex flex-col min-h-[calc(100vh-4rem)]">
      {notification.isVisible && (
        <ToastNotification {...notification} onClose={closeNotification} />
      )}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="mb-12 animate-fade-up">
          <div className="flex items-center gap-3 mb-6">
            <button
              className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground/80 transition-colors group"
              onClick={() => navigate(-1)}
            >
              <FaArrowLeft
                size={10}
                className="group-hover:-translate-x-0.5 transition-transform"
              />
              <span className="text-xs font-mono">Back</span>
            </button>
            <div className="h-3.5 w-px bg-border/50" />
            <h1 className="font-heading text-xl text-foreground/90">
              {setMetadata.setName || "Study Session"}
            </h1>
          </div>
          <div className="flex items-center justify-between">
            <p className="text-muted-foreground text-sm">
              Think of the answer, then click to reveal.
            </p>
            {data.length > 0 && currentFlashCard < data.length && (
              <span className="text-[10px] font-mono text-muted-foreground/40">
                {currentFlashCard + 1}
                <span className="text-muted-foreground/20 mx-0.5">/</span>
                {data.length}
              </span>
            )}
          </div>

          {/* Progress bar */}
          {data.length > 0 && (
            <div className="mt-4 h-px bg-border/40 rounded-full overflow-hidden">
              <div
                className="h-full bg-copper/60 transition-all duration-500 ease-out rounded-full"
                style={{
                  width: `${((currentFlashCard + (isAnswer ? 0.5 : 0)) / data.length) * 100}%`,
                }}
              />
            </div>
          )}
        </div>

        {data.length > 0 && currentFlashCard < data.length ? (
          <div className="flex-1 flex flex-col items-center">
            <FlashCard
              key={data[currentFlashCard].flashcard_id}
              setIsAnswer={setIsAnswer}
              isAnswer={isAnswer}
              data={data[currentFlashCard]}
            />
            <DifficultyButtons
              isAnswer={isAnswer}
              fcid={data[currentFlashCard].flashcard_id}
              onSkip={nextFlashCard}
              userAnswered={userAnswered}
            />
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center py-20 animate-fade-in">
            <p className="font-heading text-2xl italic text-foreground/40 mb-2">
              All caught up
            </p>
            <p className="text-sm text-muted-foreground">
              No flashcards to practice right now.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
