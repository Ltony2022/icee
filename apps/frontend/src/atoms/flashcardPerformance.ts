import { atom } from "recoil";

// Interface
export interface FlashcardPerformance {
  flashcard_id: number;
  totalFlashcards: number;
  totalReviewed: number;
  totalSkipped: number;
}

// Default value if user set nothing
const defaultPerformance: FlashcardPerformance = {
  flashcard_id: 0,
  totalFlashcards: 10,
  totalReviewed: 0,
  totalSkipped: 0,
};

// Real chad energy
const FlashcardPerformanceAtom = atom({
  key: "trackFlashcardPerformance",
  default: defaultPerformance,
});

export default FlashcardPerformanceAtom;
