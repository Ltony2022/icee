import React from "react";

interface displayFlashCard {
  setIsAnswer: React.Dispatch<React.SetStateAction<boolean>>;
  isAnswer: boolean;
  data: { answer: string; question: string };
}

export default function FlashCard({
  setIsAnswer,
  isAnswer,
  data,
}: displayFlashCard) {
  return (
    <div className="flex justify-center w-full p-4" style={{ perspective: "1200px" }}>
      <div
        className={`
          w-[580px] h-72 relative cursor-pointer
          transition-all duration-500 ease-out
          rounded-lg noise
          ${
            isAnswer
              ? "bg-card ring-1 ring-copper/20 shadow-lg shadow-copper/5"
              : "bg-card ring-1 ring-border/50 hover:ring-border"
          }
        `}
        onClick={() => setIsAnswer(!isAnswer)}
      >
        <div className="absolute inset-0 flex flex-col justify-center items-center p-10">
          {/* Label */}
          <span
            className={`absolute top-5 left-6 text-[10px] font-mono uppercase tracking-wider transition-colors duration-300 ${
              isAnswer ? "text-copper/50" : "text-muted-foreground/30"
            }`}
          >
            {isAnswer ? "Answer" : "Question"}
          </span>

          {/* Content */}
          <div className="text-center max-w-[85%]">
            <p
              className={`
                text-xl font-heading leading-relaxed
                transition-all duration-300
                ${isAnswer ? "text-foreground/95" : "text-foreground/80"}
              `}
            >
              {isAnswer ? data.answer : data.question}
            </p>
          </div>

          {/* Hint */}
          <div
            className={`
              absolute bottom-5 text-[11px] font-mono
              transition-colors duration-300
              ${isAnswer ? "text-copper/40" : "text-muted-foreground/25"}
            `}
          >
            {isAnswer ? "click to see question" : "click to reveal"}
          </div>
        </div>
      </div>
    </div>
  );
}
