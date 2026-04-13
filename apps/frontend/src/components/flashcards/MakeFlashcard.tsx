import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useState, MouseEvent, ChangeEvent } from "react";
import { Button } from "../ui/button";
import { FaPlus } from "react-icons/fa";

interface CreateFlashcardProps {
  postFlashcard: (
    event: MouseEvent<HTMLButtonElement>,
    data: { question: string; answer: string }
  ) => void;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

const CreateFlashcard = ({
  postFlashcard,
  isOpen,
  setIsOpen,
}: CreateFlashcardProps) => {
  const [data, setData] = useState({
    question: "",
    answer: "",
  });

  function handleChange(e: ChangeEvent<HTMLTextAreaElement>) {
    const { name, value } = e.target;
    setData((prev) => ({ ...prev, [name]: value }));
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <button
          onClick={() => setIsOpen(true)}
          className="inline-flex items-center gap-2 px-3.5 py-2 text-[13px] font-medium text-foreground/70 bg-card hover:bg-secondary rounded-md transition-all ring-1 ring-border/60 hover:ring-copper/30"
        >
          <FaPlus size={9} className="text-copper/70" />
          Add Card
        </button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-lg bg-card border-border/60">
        <DialogHeader>
          <DialogTitle className="font-heading text-2xl text-foreground/95">
            New Flashcard
          </DialogTitle>
          <DialogDescription className="text-muted-foreground text-sm">
            Write the question and answer for this card.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-5 py-4">
          <div>
            <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-2.5 block">
              Question (Front)
            </label>
            <textarea
              name="question"
              rows={2}
              placeholder="What is the capital of France?"
              onChange={handleChange}
              value={data.question}
              className="w-full bg-background ring-1 ring-border/60 rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/30 focus:outline-none focus:ring-copper/40 transition-all resize-none leading-relaxed"
            />
          </div>
          <div>
            <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-2.5 block">
              Answer (Back)
            </label>
            <textarea
              name="answer"
              rows={3}
              placeholder="Paris"
              onChange={handleChange}
              value={data.answer}
              className="w-full bg-background ring-1 ring-border/60 rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/30 focus:outline-none focus:ring-copper/40 transition-all resize-none leading-relaxed"
            />
          </div>
        </div>
        <DialogFooter>
          <Button
            onClick={(e) => {
              postFlashcard(e, data);
              setData({ question: "", answer: "" });
            }}
            disabled={!data.question.trim() || !data.answer.trim()}
            className="bg-copper text-copper-foreground hover:brightness-110 disabled:opacity-40"
          >
            Create Card
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default CreateFlashcard;
