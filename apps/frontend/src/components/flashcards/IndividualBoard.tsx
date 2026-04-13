import React from "react";

import BoardCard, { CardDataProps } from "./BoardCard";

export interface BoardDataType {
  id: number;
  header: string;
}

export interface individualBoardProps extends BoardDataType {
  // cardData: InternalBoardCardProps[];
  cardData: CardDataProps[];
}

function handleDragStart(e: React.DragEvent) {
  console.log("dragged");
  e.dataTransfer.setData("id", e.currentTarget.id);
}

function handleDragEnter(e: React.DragEvent) {
  e.preventDefault();
  console.log("dragged over");
}

function onDragOver(e: React.DragEvent) {
  e.preventDefault();
}

function onDrop(e: React.DragEvent) {
  e.preventDefault();
  const data = e.dataTransfer.getData("id");
  console.log(data);
}

export const IndividualBoard = ({
  id,
  header,
  cardData,
}: individualBoardProps) => {
  return (
    <div
      className={
        "border-2 border-slate-500 w-80 h-full mt-4 ml-4 p-2 overflow-hidden"
      }
      id={id.toString()}
      onDragOver={onDragOver}
      onDrop={onDrop}
    >
      <h1>{header}</h1>
      <div className={"mt-4 mb-2"}>
        {cardData.map((card, index) => (
          <BoardCard
            key={index}
            title={card.title}
            description={card.description}
            taskId={card.taskId}
            draggable
            handleDragStart={handleDragStart}
            handleDragEnter={handleDragEnter}
          />
        ))}
      </div>
    </div>
  );
};
