import FlashcardPerformanceAtom from "@/atoms/flashcardPerformance";
import { useCallback } from "react";
import { useRecoilState } from "recoil";

const useFlashcardPerformanceTracker = () => {
  // state related to flashcard performance
  const [performance, setPerformance] = useRecoilState(FlashcardPerformanceAtom);
  // let setPerformance = useSetRecoilState(FlashcardPerformanceAtom);
  // return the total number of flashcards, reviewed, and skipped

  const calculateSkipped = useCallback(() => {
    setPerformance((old) => ({
      ...old,
      totalSkipped: old.totalFlashcards - old.totalReviewed,
    }));
  }, [setPerformance]);

  const setFlashcardsTotalNumber = useCallback(
    (total: number) => {
      setPerformance((old) => ({
        ...old,
        totalFlashcards: total,
      }));
    },
    [setPerformance]
  );

  const addReviewed = useCallback(() => {
    setPerformance((old) => ({
      ...old,
      totalReviewed: old.totalReviewed + 1,
    }));
  }, [setPerformance]);

  const resetPerformance = useCallback(() => {
    setPerformance((old) => ({
      ...old,
      totalFlashcards: 0,
      totalReviewed: 0,
      totalSkipped: 0,
    }));
  }, [setPerformance]);

  return {
    totalFlashcards: performance.totalFlashcards,
    totalReviewed: performance.totalReviewed,
    totalSkipped: performance.totalSkipped,
    calculateSkipped,
    setTotalFlashcards: setFlashcardsTotalNumber,
    addReviewed,
    resetPerformance,
  };
};

export default useFlashcardPerformanceTracker;
