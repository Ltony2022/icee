import EditFlashcard, { FlashcardForm } from "@/atoms/modifyFlashcardsForm";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { getBackendOrigin } from "@/config/backendOrigin";
import { useRecoilState } from "recoil";

export function FlashcardEditDialog({
  set_id,
  refreshData,
}: {
  set_id?: string;
  refreshData: () => void;
}) {
  const [editData, setEditData] = useRecoilState<FlashcardForm>(EditFlashcard);

  // Submit update to the server
  async function saveEdit() {
    const data = {
      flashcard_id: Number(editData.flashcard_id),
      question: editData.question,
      answer: editData.answer,
    };
    // send the data to the server
    await axios.put(
      `${getBackendOrigin()}/flashcards/set/${set_id}/update`,
      data
    );
    refreshData();
    // close the dialog
    closeDialog();
  }

  function closeDialog() {
    setEditData({
      ...editData,
      isOpen: false,
    });
    // unmound the dialog
  }

  return (
    <Dialog
      open={editData.isOpen && editData.mode === "edit"}
      onOpenChange={closeDialog}
    >
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit flashcard</DialogTitle>
          <DialogDescription>
            Updating your flashcard is easy. Just change the fields below and
            click save.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="question" className="text-right">
              Question
            </Label>
            <Input
              id="question"
              defaultValue={editData.question}
              className="col-span-3"
              onChange={(e) => {
                setEditData({ ...editData, question: e.target.value });
              }}
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="answer" className="text-right">
              Answer
            </Label>
            <Input
              id="answer"
              defaultValue={editData.answer}
              className="col-span-3"
              onChange={(e) => {
                setEditData({ ...editData, answer: e.target.value });
              }}
            />
          </div>
        </div>
        <DialogFooter>
          <Button onClick={saveEdit}>
            Save changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
