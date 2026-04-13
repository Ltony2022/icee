import { Link, useLocation } from "react-router-dom";
import { FaPlay, FaBan, FaClone, FaCog, FaShieldAlt } from "react-icons/fa";
import { HiOutlineViewGrid } from "react-icons/hi";

const links = [
  { name: "Overview", path: "/", icon: <HiOutlineViewGrid size={16} /> },
  { name: "Focus", path: "/pomodoro", icon: <FaPlay size={11} /> },
  { name: "Flashcards", path: "/user-flashcards", icon: <FaClone size={13} /> },
  { name: "Blocker", path: "/network-blocker", icon: <FaBan size={13} /> },
  { name: "App Blocker", path: "/application-blocker", icon: <FaShieldAlt size={13} /> },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-[220px] h-full bg-card flex flex-col shrink-0 border-r border-border/60">
      {/* Brand */}
      <div className="px-5 pt-7 pb-8">
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-7 h-7 rounded-md bg-copper/15 flex items-center justify-center shrink-0 ring-1 ring-copper/20">
            <span className="text-copper font-heading text-base leading-none translate-y-[1px]">I</span>
          </div>
          <span className="font-heading text-[1.15rem] text-foreground/90 tracking-tight">
            ICEEUtils
          </span>
        </Link>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 space-y-0.5">
        <p className="px-3 mb-3 text-[10px] font-mono font-medium text-muted-foreground/60 uppercase tracking-[0.15em]">
          Navigate
        </p>
        {links.map((link) => {
          const isActive =
            location.pathname === link.path ||
            (link.path !== "/" && location.pathname.startsWith(link.path));
          return (
            <Link
              key={link.path}
              to={link.path}
              className={`flex items-center gap-3 px-3 py-2 rounded-md text-[13px] font-medium transition-all duration-200 group relative ${
                isActive
                  ? "text-foreground bg-secondary"
                  : "text-muted-foreground hover:text-foreground/80 hover:bg-secondary/50"
              }`}
            >
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-4 rounded-r-full bg-copper" />
              )}
              <span
                className={`text-sm transition-colors ${
                  isActive
                    ? "text-copper"
                    : "text-muted-foreground/60 group-hover:text-muted-foreground"
                }`}
              >
                {link.icon}
              </span>
              {link.name}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-border/40">
        <div className="flex items-center gap-3 px-3 py-2 text-[13px] font-medium text-muted-foreground hover:text-foreground/80 rounded-md hover:bg-secondary/50 cursor-pointer transition-colors group">
          <span className="text-sm text-muted-foreground/60 group-hover:text-muted-foreground">
            <FaCog size={13} />
          </span>
          Settings
        </div>
      </div>
    </aside>
  );
}
