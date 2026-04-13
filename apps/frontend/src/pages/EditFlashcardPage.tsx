import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useState } from "react";
import { toast } from "react-hot-toast";
import { useNavigate, useParams } from "react-router-dom";
import { useRecoilState } from "recoil";
import EditFlashcard, { FlashcardForm } from "../atoms/modifyFlashcardsForm";
import { FaTrash } from "react-icons/fa";

const EditFlashcardPage = () => {
  const setId = useParams().setId;
  const [editingFlashcard, setEditingFlashcard] =
    useRecoilState<FlashcardForm>(EditFlashcard);
  const [isSaving, setIsSaving] = useState(false);
  const navigate = useNavigate();

  const handleSave = async () => {
    setIsSaving(true);
    await axios
      .put(`${getBackendOrigin()}/flashcards/set/${setId}/update`, {
        flashcard_id: editingFlashcard.flashcard_id,
        question: editingFlashcard.question,
        answer: editingFlashcard.answer,
      })
      .then(() => toast.success("Saved"))
      .catch(() => toast.error("Failed to save"));
    setIsSaving(false);
  };

  const handleDelete = async () => {
    setIsSaving(true);
    await axios
      .delete(`${getBackendOrigin()}/flashcards/set/${setId}/delete`, {
        data: {
          flashcard_id: editingFlashcard.flashcard_id,
          question: editingFlashcard.question,
          answer: editingFlashcard.answer,
          mode: editingFlashcard.mode,
        },
      })
      .then(() => {
        toast.success("Card deleted");
        navigate(`/flashcard/${setId}/manage`);
      })
      .catch(() => toast.error("Failed to delete"));
    setIsSaving(false);
  };

  if (!editingFlashcard.question) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-muted-foreground/40">
        <p className="font-heading text-xl italic text-foreground/20 mb-1">
          No card selected
        </p>
        <p className="text-xs font-mono text-muted-foreground/30">
          Pick a question from the left panel
        </p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col p-7 animate-slide-in-right">
      {/* Header */}
      <div className="mb-7 flex items-center justify-between">
        <div>
          <h2 className="font-heading text-2xl text-foreground/90">
            Edit Card
          </h2>
          <p className="text-[10px] font-mono text-muted-foreground/40 mt-1">
            ID {editingFlashcard.flashcard_id}
          </p>
        </div>
        <button
          onClick={handleDelete}
          disabled={isSaving}
          className="inline-flex items-center gap-2 text-xs font-mono text-muted-foreground/50 hover:text-destructive transition-colors disabled:opacity-40"
          title="Delete this card"
        >
          <FaTrash size={10} />
          delete
        </button>
      </div>

      {/* Form */}
      <div className="flex-1 flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em]">
            Front — Question
          </label>
          <textarea
            rows={3}
            className="w-full bg-background ring-1 ring-border/50 rounded-md px-4 py-3 text-sm text-foreground/90 placeholder:text-muted-foreground/25 focus:outline-none focus:ring-copper/40 transition-all resize-none leading-relaxed"
            value={editingFlashcard.question}
            onChange={(e) =>
              setEditingFlashcard({
                ...editingFlashcard,
                question: e.target.value,
              })
            }
          />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em]">
            Back — Answer
          </label>
          <textarea
            rows={6}
            className="w-full bg-background ring-1 ring-border/50 rounded-md px-4 py-3 text-sm text-foreground/90 placeholder:text-muted-foreground/25 focus:outline-none focus:ring-copper/40 transition-all resize-none leading-relaxed"
            value={editingFlashcard.answer}
            onChange={(e) =>
              setEditingFlashcard({
                ...editingFlashcard,
                answer: e.target.value,
              })
            }
          />
        </div>

        {/* Save */}
        <div className="mt-auto pt-5 flex justify-end">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="px-5 py-2.5 rounded-md bg-copper text-copper-foreground text-sm font-medium hover:brightness-110 transition-all disabled:opacity-40 shadow-sm shadow-copper/10"
          >
            {isSaving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditFlashcardPage;
