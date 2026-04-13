import CreateFlashcard from "@/components/flashcards/MakeFlashcard";
import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { Link, Outlet, useParams } from "react-router-dom";
import { useSetRecoilState } from "recoil";
import EditFlashcard, { FlashcardForm } from "../atoms/modifyFlashcardsForm";
import { FaArrowLeft, FaPlus } from "react-icons/fa";

const ManageFlashcardSet = () => {
  const { setId } = useParams();

  const [clickedLink, setClickedLink] = useState<string>("");
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [setOfFlashcard, setSetOfFlashcard] = useState<FlashcardForm[]>([]);
  const setEditingFlashcard = useSetRecoilState<FlashcardForm>(EditFlashcard);

  async function fetchData() {
    const response = await axios.get(
      `${getBackendOrigin()}/flashcards/set/${setId}`
    );
    setSetOfFlashcard(response.data);
  }

  useEffect(() => {
    fetchData();
  }, [setId]);

  async function createFlashcard(
    e: React.MouseEvent<HTMLButtonElement>,
    flashcard: { question: string; answer: string }
  ) {
    e.preventDefault();
    await axios
      .post(`${getBackendOrigin()}/flashcards/set/${setId}/create`, flashcard)
      .then(() => {
        toast.success("Flashcard created");
        setIsOpen(false);
        fetchData();
      })
      .catch(() => {
        toast.error("Failed to create flashcard");
      });
  }

  function setFlashcard(flashcard: FlashcardForm) {
    setEditingFlashcard({
      flashcard_id: flashcard.flashcard_id,
      mode: "edit",
      question: flashcard.question,
      answer: flashcard.answer,
      isOpen: true,
    });
  }

  return (
    <div className="w-full h-full flex flex-col animate-fade-in">
      {/* Top bar */}
      <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-border/50">
        <div className="flex items-center gap-4">
          <Link
            to={`/flashcard/${setId}/manage`}
            className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground/80 transition-colors group"
          >
            <FaArrowLeft
              size={10}
              className="group-hover:-translate-x-0.5 transition-transform"
            />
            <span className="text-xs font-mono">Back</span>
          </Link>
          <div className="w-px h-4 bg-border/50" />
          <h1 className="font-heading text-lg text-foreground/90">
            Manage Cards
          </h1>
          <span className="text-[10px] font-mono text-muted-foreground/40">
            {setOfFlashcard.length}
          </span>
        </div>
        <CreateFlashcard
          postFlashcard={createFlashcard}
          isOpen={isOpen}
          setIsOpen={setIsOpen}
        />
      </div>

      {/* Split panel */}
      <div className="flex-1 flex min-h-0">
        {/* Left: Card list */}
        <div className="w-72 shrink-0 border-r border-border/40 flex flex-col bg-background">
          <div className="px-4 py-3 border-b border-border/40 flex items-center justify-between">
            <p className="text-[10px] font-mono font-medium text-muted-foreground/40 uppercase tracking-[0.15em]">
              Questions
            </p>
            <button
              onClick={() => setIsOpen(true)}
              className="w-5 h-5 rounded bg-secondary hover:bg-copper/15 flex items-center justify-center text-muted-foreground/50 hover:text-copper transition-colors"
              title="Add card"
            >
              <FaPlus size={8} />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-2 py-1.5 space-y-px">
            {setOfFlashcard.map((flashcard) => {
              const linkPath = `/flashcard/${setId}/manageFlashcardSet/card/${flashcard.flashcard_id}`;
              const isActive = clickedLink === linkPath;
              return (
                <Link
                  to={linkPath}
                  className={`block px-3 py-2.5 rounded-md text-[13px] transition-all duration-150 leading-relaxed ${
                    isActive
                      ? "bg-copper/10 text-copper ring-1 ring-copper/15"
                      : "text-muted-foreground hover:bg-secondary/60 hover:text-foreground/70"
                  }`}
                  key={flashcard.flashcard_id}
                  onClick={() => {
                    setFlashcard(flashcard);
                    setClickedLink(linkPath);
                  }}
                >
                  <div className="line-clamp-2">{flashcard.question}</div>
                </Link>
              );
            })}
            {setOfFlashcard.length === 0 && (
              <div className="flex flex-col items-center justify-center py-16 text-center">
                <p className="font-heading text-base italic text-foreground/30">
                  Empty set
                </p>
                <p className="text-xs text-muted-foreground/40 mt-1">
                  Click + to create your first card
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Detail/edit panel */}
        <div className="flex-1 min-w-0 bg-card/30">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default ManageFlashcardSet;
