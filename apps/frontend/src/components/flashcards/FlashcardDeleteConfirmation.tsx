import EditFlashcard, { FlashcardForm } from "@/atoms/modifyFlashcardsForm";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { useRecoilState } from "recoil";

export function FlashcardDeleteConfirmation({
  deleteAction,
}: {
  deleteAction: () => void | Promise<void>;
}) {
  const [deleteData, setDeleteData] =
    useRecoilState<FlashcardForm>(EditFlashcard);

  // Function for closing the dialog
  function closeDialog() {
    setDeleteData((prev) => ({
      ...prev,
      isOpen: false,
    }));
  }

  return (
    <AlertDialog open={deleteData.isOpen && deleteData.mode === "delete"}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete your
            account and remove your data from our servers.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={closeDialog}>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={deleteAction}>Continue</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
