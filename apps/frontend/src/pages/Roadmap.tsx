import { CardDataProps } from "@/components/flashcards/BoardCard";
import { IndividualBoard } from "@/components/flashcards/IndividualBoard";
import { LaneData } from "@/data/laneDemo.ts";
import { tasks } from "@/data/tasksDemo.ts";
import { useState } from "react";

export default function Roadmap() {
  const [taskData] = useState<CardDataProps[]>(tasks);

  return (
    <div>
      <h1 className="text-6xl mt-8 ml-8">Roadmap</h1>
      <div className={"flex w-full h-full items-center"}>
        {LaneData.map((lane) => (
          <IndividualBoard
            key={lane.id}
            id={lane.id}
            header={lane.header}
            cardData={taskData.filter(
              (task: CardDataProps) => task.laneId === lane.id
            )}
          />
        ))}
      </div>
    </div>
  );
}
