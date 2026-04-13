import { LuConstruction } from "react-icons/lu";
import { useNavigate } from "react-router-dom";
import { Button } from "../ui/button";

export interface DisplayCardProps {
  title: string;
  details: string;
  link: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  colorTheme?: "primary" | "indigo" | "rose" | "emerald";
}

const themeStyles = {
  primary: "bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground",
  indigo: "bg-indigo-100 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white",
  rose: "bg-rose-100 text-rose-600 group-hover:bg-rose-600 group-hover:text-white",
  emerald: "bg-emerald-100 text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white",
};

const DisplayCard = ({
  title,
  details,
  link,
  icon: Icon = LuConstruction,
  colorTheme = "primary",
}: DisplayCardProps) => {
  const navigate = useNavigate();
  const themeClass = themeStyles[colorTheme] || themeStyles.primary;

  return (
    <div className="group relative flex h-full flex-col justify-between overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
      <div>
        <div className="mb-6 flex items-center justify-between">
          <div
            className={`flex h-14 w-14 items-center justify-center rounded-xl transition-colors duration-300 ${themeClass}`}
          >
            <Icon size={24} className="transition-transform duration-300 group-hover:scale-110" />
          </div>
        </div>
        <h3 className="font-heading mb-3 text-2xl font-semibold text-slate-800">
          {title || "Feature"}
        </h3>
        <p className="mb-8 text-base leading-relaxed text-slate-500">
          {details || "Coming soon..."}
        </p>
      </div>

      <Button
        variant="outline"
        className="w-full rounded-xl border-slate-200 py-6 text-sm font-medium transition-colors hover:bg-slate-50 hover:text-slate-900 group-hover:border-slate-300"
        onClick={() => {
          if (link) navigate(link);
        }}
      >
        {link ? "Get Started" : "Coming Soon"}
      </Button>
    </div>
  );
};

export default DisplayCard;
