import { Button } from "@/components/ui/button.tsx";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog.tsx";
import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaPlus } from "react-icons/fa";

const CreateFlashcardSet = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [setName, setSetName] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  async function submitForm() {
    if (!setName.trim()) return;
    setIsSubmitting(true);
    try {
      const response = await axios.post(
        `${getBackendOrigin()}/flashcards/set/new`,
        { set_name: setName }
      );
      setIsOpen(false);
      setSetName("");
      if (response.data?.setId) {
        navigate(`/flashcard/${response.data.setId}/manageFlashcardSet`);
      } else {
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && setName.trim()) {
      submitForm();
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <button className="inline-flex items-center gap-2 px-3.5 py-2 text-[13px] font-medium text-foreground/70 bg-card hover:bg-secondary rounded-md transition-all cursor-pointer ring-1 ring-border/60 hover:ring-copper/30">
          <FaPlus size={9} className="text-copper/70" />
          New Set
        </button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md bg-card border-border/60">
        <DialogHeader>
          <DialogTitle className="font-heading text-2xl text-foreground/95">
            New set
          </DialogTitle>
          <DialogDescription className="text-muted-foreground text-sm">
            Give your flashcard set a name to begin adding cards.
          </DialogDescription>
        </DialogHeader>
        <div className="py-5">
          <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-2.5 block">
            Set Name
          </label>
          <input
            type="text"
            placeholder="e.g. Biology Chapter 4, React Hooks..."
            value={setName}
            onChange={(e) => setSetName(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
            className="w-full bg-background ring-1 ring-border/60 rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/30 focus:outline-none focus:ring-copper/40 transition-all"
          />
        </div>
        <DialogFooter>
          <Button
            onClick={submitForm}
            disabled={!setName.trim() || isSubmitting}
            className="bg-copper text-copper-foreground hover:brightness-110 disabled:opacity-40"
          >
            {isSubmitting ? "Creating..." : "Create Set"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default CreateFlashcardSet;
