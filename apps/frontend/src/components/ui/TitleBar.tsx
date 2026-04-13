import React from "react";

export const TitleBar = () => {
  // export a variable that tracks maximized state
  const [isMaximized, setIsMaximized] = React.useState(false);
  const handleMinimize = () => {
    window.ipcRenderer.send("minimizeApp");
  };

  const handleMaximize = () => {
    window.ipcRenderer.send("maximize-window");
    setIsMaximized(!isMaximized);
  };

  const handleClose = () => {
    window.ipcRenderer.send("close-window");
  };

  // handle when the title bar is hovered
  const handleHover = () => {
    console.log("hovered");

    // allow the user to drag the window
    window.ipcRenderer.send("drag-window");
  };

  // handle when the title bar is clicked

  return (
    <div
      className="flex justify-between items-center bg-gray-800 text-white h-10 px-4 titlebar"
      onMouseDown={handleHover}
    >
      <div className="flex-1 text-center">
        <span className="text-lg">My Electron App</span>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={handleMinimize}
          className="hover:bg-gray-700 p-1 rounded"
        >
          _
        </button>
        <button
          onClick={handleMaximize}
          className="hover:bg-gray-700 p-1 rounded"
        >
          {isMaximized ? "▣" : "□"}
        </button>
        <button onClick={handleClose} className="hover:bg-red-700 p-1 rounded">
          ✕
        </button>
      </div>
    </div>
  );
};
