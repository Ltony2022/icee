import ListOfCards from "../flashcards/ListOfCards";
import { Link } from "react-router-dom";

export default function HomeSection() {
  return (
    <div>
      <h1 className="pl-12 text-[25px] font-bold">Other section</h1>
      <ListOfCards type="other" />

      {/* A link to the new homepage */}
      <Link to="/new-homepage" className="text-blue-500 hover:underline">
        Go to the new homepage
      </Link>
    </div>
  );
}
