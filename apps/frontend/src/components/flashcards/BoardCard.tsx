import React from "react";

export interface CardDataProps {
  laneId?: number;
  title: string;
  description: string;
  taskId: number;
}

export interface InternalBoardCardProps extends CardDataProps {
  draggable: boolean;
  handleDragStart: (event: React.DragEvent) => void;
  handleDragEnter: (event: React.DragEvent) => void;
}

const BoardCard = ({
  title,
  description,
  taskId,
  draggable,
  handleDragStart,
  handleDragEnter,
}: InternalBoardCardProps) => {
  return (
    <div
      className={"border-2 border-black p-2"}
      draggable={draggable}
      id={taskId.toString()}
      onDragStart={handleDragStart}
      onDragEnter={handleDragEnter}
    >
      <h1>{title}</h1>
      <p>{description}</p>
    </div>
  );
};
export default BoardCard;
