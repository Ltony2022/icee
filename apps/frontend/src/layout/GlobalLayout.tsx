import { Sidebar } from "@/components/layout/Sidebar";
import { Outlet } from "react-router-dom";

const GlobalLayout = () => {
  return (
    <div className="h-screen w-screen flex overflow-hidden bg-background text-foreground selection:bg-copper/20 selection:text-copper">
      <Sidebar />
      <main className="flex-1 h-full overflow-y-auto overflow-x-hidden relative flex flex-col">
        <Outlet />
      </main>
    </div>
  );
};

export default GlobalLayout;
