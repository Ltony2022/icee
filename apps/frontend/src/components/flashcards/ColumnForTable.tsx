"use client";

import { ColumnDef } from "@tanstack/react-table";
import { MoreHorizontal } from "lucide-react";

import EditFlashcard, { FlashcardForm } from "@/atoms/modifyFlashcardsForm";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Dialog } from "@radix-ui/react-dialog";
import { useRecoilState } from "recoil";

// Define flashcard row
export type FlashcardRow = {
  flashcard_id: string;
  question: string;
  answer: string;
};

export const ColumnsForFlashcard: ColumnDef<FlashcardRow>[] = [
  {
    accessorKey: "flashcard_id",
    header: "Flashcard ID",
  },
  {
    accessorKey: "question",
    header: "Question",
  },
  {
    accessorKey: "answer",
    header: "Answer",
  },
  // Actions
  {
    id: "actions",
    cell: ({ row }) => {
      const flashcard = row.original;

      // Necessary for editing the flashcard
      const [editFlashcard, setEditFlashcard] =
        // since tanstack/react-table is not a hook, we can't use it here
        // because of this being passed to the table component, we can't use hooks or pass props
        // to circumvent this, temporarily disable the eslint rule and use a global state management (recoil)
        // eslint-disable-next-line react-hooks/rules-of-hooks
        useRecoilState<FlashcardForm>(EditFlashcard);

      // Function for toggling the edit flashcard form
      function toggleEditFlashcardForm(data: FlashcardRow) {
        setEditFlashcard({
          mode: "edit",
          flashcard_id: Number(data.flashcard_id),
          question: data.question,
          answer: data.answer,
          isOpen: !editFlashcard.isOpen,
        });
      }

      // Function that toggles the delete flashcard form
      function toggleDeleteFlashcardForm(flashcard_id: number) {
        setEditFlashcard({
          mode: "delete",
          flashcard_id: Number(flashcard_id),
          isOpen: !editFlashcard.isOpen,
        });
      }

      return (
        <Dialog>
          <DropdownMenu modal={false}>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem
                onClick={() => {
                  toggleEditFlashcardForm(flashcard);
                }}
              >
                Edit flashcard
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="text-red-400"
                onClick={() => {
                  toggleDeleteFlashcardForm(Number(flashcard.flashcard_id));
                }}
              >
                Delete flashcard
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </Dialog>
      );
    },
  },
];
