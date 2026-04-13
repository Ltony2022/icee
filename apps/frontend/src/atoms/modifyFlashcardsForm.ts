import { atom } from "recoil";



// Default value if user set nothing
const defaultFlashcardManageForm: FlashcardForm = {
  mode: "edit",
  flashcard_id: 0,
  question: "",
  answer: "",
  isOpen: false,
};

// Real chad energy
const EditFlashcard = atom({
  key: "editFlashcardForm",
  default: defaultFlashcardManageForm,
});

export default EditFlashcard;

// Interface
export interface FlashcardForm {
  flashcard_id: number;
  mode: "edit" | "delete";
  question?: string;
  answer?: string;
  isOpen: boolean;
}
