import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { appLink } from "./constant/AppLink.tsx";
import "./index.css";
// Use recoil for global state management
import { RecoilRoot } from "recoil";
import FocusApplet from "./components/FocusApplet.tsx";
import { Toaster } from "react-hot-toast";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <div className="">
    <RecoilRoot>
      <Toaster />
      <FocusApplet />
      <RouterProvider router={appLink} />
    </RecoilRoot>
  </div>
);

// Use contextBridge
window.ipcRenderer.on("main-process-message", (_event, message) => {
  console.log(message);
});
