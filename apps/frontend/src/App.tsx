import { FaBan, FaPlay, FaClone } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const tools = [
  {
    name: "Focus Session",
    desc: "Start an uninterrupted Pomodoro timer",
    path: "/pomodoro",
    icon: <FaPlay size={13} className="ml-0.5" />,
    accent: "text-amber-400",
    accentBg: "bg-amber-500/10 ring-amber-500/15",
  },
  {
    name: "Flashcards",
    desc: "Review your spaced repetition decks",
    path: "/user-flashcards",
    icon: <FaClone size={14} />,
    accent: "text-copper",
    accentBg: "bg-copper/10 ring-copper/15",
  },
  {
    name: "Network Blocker",
    desc: "Manage blocked applications and domains",
    path: "/network-blocker",
    icon: <FaBan size={14} />,
    accent: "text-rose-400",
    accentBg: "bg-rose-500/10 ring-rose-500/15",
  },
];

export default function App() {
  const navigate = useNavigate();

  return (
    <div className="p-10 max-w-3xl w-full mx-auto h-full flex flex-col">
      {/* Hero */}
      <div className="mb-16 mt-10 animate-fade-up">
        <h1 className="font-heading text-5xl text-foreground/95 tracking-tight leading-[1.1]">
          Your study
          <br />
          <span className="italic text-copper">environment</span> is ready.
        </h1>
        <p className="text-muted-foreground mt-4 text-[15px] max-w-md leading-relaxed">
          Focus, memorize, and stay on track. Everything you need in one place.
        </p>
      </div>

      <div className="space-y-12 flex-1">
        {/* Tools */}
        <div className="animate-fade-up" style={{ animationDelay: "100ms" }}>
          <p className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-4 ml-1">
            Quick Launch
          </p>
          <div className="flex flex-col gap-1">
            {tools.map((tool) => (
              <button
                key={tool.path}
                onClick={() => navigate(tool.path)}
                className="w-full group flex items-center justify-between px-4 py-3.5 rounded-lg hover:bg-secondary/60 transition-all duration-200 text-left cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div
                    className={`w-9 h-9 rounded-lg ${tool.accentBg} ring-1 flex items-center justify-center ${tool.accent} transition-all`}
                  >
                    {tool.icon}
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground/90 text-sm">
                      {tool.name}
                    </h3>
                    <p className="text-[13px] text-muted-foreground mt-0.5">
                      {tool.desc}
                    </p>
                  </div>
                </div>
                <span className="text-xs font-mono text-muted-foreground/40 group-hover:text-copper transition-colors duration-200 opacity-0 group-hover:opacity-100 -translate-x-1 group-hover:translate-x-0">
                  open
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="animate-fade-up" style={{ animationDelay: "200ms" }}>
          <p className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-4 ml-1">
            Today
          </p>
          <div className="flex items-center gap-0 rounded-lg bg-card ring-1 ring-border/60 overflow-hidden noise">
            {[
              { label: "Focus", value: "0", unit: "min" },
              { label: "Cards Due", value: "0", unit: "" },
              { label: "Blocked", value: "0", unit: "" },
            ].map((stat, i) => (
              <div
                key={stat.label}
                className={`flex-1 px-6 py-5 ${i < 2 ? "border-r border-border/40" : ""}`}
              >
                <p className="text-[10px] font-mono text-muted-foreground/50 uppercase tracking-wider mb-2">
                  {stat.label}
                </p>
                <p className="font-heading text-3xl text-foreground/80 tracking-tight">
                  {stat.value}
                  {stat.unit && (
                    <span className="text-sm font-sans font-normal text-muted-foreground/40 ml-1">
                      {stat.unit}
                    </span>
                  )}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
