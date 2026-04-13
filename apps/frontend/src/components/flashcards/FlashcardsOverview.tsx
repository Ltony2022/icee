import { Separator } from "../ui/separator";

interface displayOverview {
  number: number;
  dataName: string;
}

// For individual component in flashcard overview
// Since the dataToDisplay is the whole interface (and it didn't exist in the interface), we use destructuring to bind the prop with the interface
function PieceOfData({
  dataToDisplay,
  className,
}: {
  dataToDisplay: displayOverview;
  className?: string;
}) {
  return (
    <div className={className}>
      <h1 className="font-bold text-3xl">{dataToDisplay.number}</h1>
      <h2 className="text-sm text-gray-400">{dataToDisplay.dataName}</h2>
    </div>
  );
}

const FlashcardsOverview = ({ data }: { data: { needReview: number; totalFlashcards: number } }) => {
  return (
    <div className="bg-gray-300 mt-4 mb-4 border border-black p-4 flex flex-row w-64">
      <PieceOfData
        dataToDisplay={{
          number: data.needReview,
          dataName: "Need review",
        }}
      />
      <Separator orientation="vertical" className="bg-gray-400 ml-4 mr-4" />
      <PieceOfData
        dataToDisplay={{
          number: data.totalFlashcards,
          dataName: "Total flashcards",
        }}
      />
    </div>
  );
};

export default FlashcardsOverview;
