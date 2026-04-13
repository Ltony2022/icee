import { createBrowserRouter, createHashRouter } from "react-router-dom";

// Pages
import App from "@/App";
import NotFound from "@/pages/common/NotFound";
import FlashcardWhenDone from "@/pages/FlashcardWhenDone";
import FlashCardPage from "@/pages/LearnFlashcard";
import ManageFlashcardSet from "@/pages/ManageFlashcardSet";
import NetworkBlocker from "@/pages/NetworkBlocker";
import ApplicationBlocker from "@/pages/ApplicationBlocker";
import Roadmap from "@/pages/Roadmap.tsx";
import UserFlashcards from "@/pages/ViewAllFlashcardSets";
import WelcomeGuide from "@/pages/WelcomeGuide";
import ManageFlashCard from "../pages/FlashcardSetOverview";
import Pomodoro from "../pages/Pomodoro";
import EditFlashcardPage from "@/pages/EditFlashcardPage";
import GlobalLayout from "@/layout/GlobalLayout";

const routes = [
  {
    path: "/",
    element: <GlobalLayout />,
    children: [
      {
        path: "/",
        element: <App />,
      },
      {
        path: "/newTest",
        element: <WelcomeGuide />,
      },
      {
        path: "/pomodoro",
        element: <Pomodoro />,
      },
      {
        path: "/network-blocker",
        element: <NetworkBlocker />,
      },
      {
        path: "/application-blocker",
        element: <ApplicationBlocker />,
      },
      {
        path: "/flashcard/:setId/learn",
        element: <FlashCardPage />,
      },
      {
        path: "/flashcard/:setId/manage",
        element: <ManageFlashCard />,
      },
      {
        path: "/flashcard/:setId/done",
        element: <FlashcardWhenDone />,
      },
      {
        path: "/user-flashcards",
        element: <UserFlashcards />,
      },
      {
        path: "/roadmap",
        element: <Roadmap />,
      },
      {
        path: "/flashcard/:setId/manageFlashcardSet",
        element: <ManageFlashcardSet />,
        children: [
          {
            path: "card/:cardId",
            element: <EditFlashcardPage key={window.location.pathname} />,
          },
        ],
      },
    ],
    errorElement: <NotFound />,
  },
];

function isFileProtocol() {
  return typeof window !== "undefined" && window.location.protocol === "file:";
}

export const appLink = isFileProtocol() ? createHashRouter(routes) : createBrowserRouter(routes);
