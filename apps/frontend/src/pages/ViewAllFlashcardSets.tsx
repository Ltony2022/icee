import CreateFlashcardSet from "@/components/flashcards/CreateFlashcardSet";
import FlashcardSet from "@/components/flashcards/FlashcardSet";
import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useState, useEffect } from "react";

export interface flashcardSetProps {
  name: string;
  numberOfCards: number;
  nextLearningDay: string;
  setId: number;
  needReview: number;
}

export default function UserFlashcards() {
  const [setOfFlashcard, setSetOfFlashcard] = useState<flashcardSetProps[]>([]);

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`${getBackendOrigin()}/flashcards/set`);
      setSetOfFlashcard(response.data);
    }
    fetchData();
  }, []);

  return (
    <div className="w-full h-full flex flex-col px-10 py-10 mx-auto max-w-4xl">
      {/* Header */}
      <div className="mb-12 animate-fade-up">
        <h1 className="font-heading text-4xl text-foreground/95 tracking-tight">
          Your <span className="italic text-copper">Flashcards</span>
        </h1>
        <p className="text-muted-foreground mt-1.5 text-sm max-w-lg">
          Spaced repetition decks for efficient memorization. Create sets, add
          cards, and study smart.
        </p>
      </div>

      {/* Toolbar */}
      <div
        className="flex items-center justify-between mb-6 animate-fade-up"
        style={{ animationDelay: "80ms" }}
      >
        <p className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em]">
          {setOfFlashcard.length} set{setOfFlashcard.length !== 1 ? "s" : ""}
        </p>
        <CreateFlashcardSet />
      </div>

      {/* Grid */}
      <div
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 animate-fade-up"
        style={{ animationDelay: "140ms" }}
      >
        {setOfFlashcard.length > 0 ? (
          setOfFlashcard.map((data, index) => (
            <FlashcardSet
              key={data.setId}
              {...data}
              style={{ animationDelay: `${160 + index * 50}ms` }}
            />
          ))
        ) : (
          <div className="col-span-full rounded-lg border border-dashed border-border/60 py-20 text-center">
            <p className="font-heading text-xl text-foreground/60 italic mb-2">
              No sets yet
            </p>
            <p className="text-sm text-muted-foreground">
              Create your first flashcard set to get started.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
