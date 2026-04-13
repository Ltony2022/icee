import { useState, useEffect, useMemo } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FaPlus, FaCheck } from "react-icons/fa";
import { getBackendOrigin } from "@/config/backendOrigin";
import type { InstalledApplication } from "@/types/applicationBlocker";

const API_BASE = `${getBackendOrigin()}/api/application-blocker`;

interface AddBlockDialogProps {
  onApplicationAdded: () => void;
}

export function AddBlockDialog({ onApplicationAdded }: AddBlockDialogProps) {
  const [installedApps, setInstalledApps] = useState<InstalledApplication[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [search, setSearch] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;

    setIsLoading(true);
    setError("");
    setSelected(new Set());
    setSearch("");

    axios
      .get(`${API_BASE}/installed/`)
      .then((res) => {
        const apps = res.data.installed_applications ?? [];
        const seen = new Set<string>();
        const unique = apps.filter((app: { executable: string }) => {
          if (seen.has(app.executable)) return false;
          seen.add(app.executable);
          return true;
        });
        setInstalledApps(unique);
      })
      .catch(() => {
        setError("Failed to load installed applications");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [open]);

  const filtered = useMemo(() => {
    if (!search) return installedApps;
    const query = search.toLowerCase();
    return installedApps
      .filter((app) => app.display_name.toLowerCase().includes(query))
      .sort((a, b) => {
        const aStarts = a.display_name.toLowerCase().startsWith(query);
        const bStarts = b.display_name.toLowerCase().startsWith(query);
        if (aStarts && !bStarts) return -1;
        if (!aStarts && bStarts) return 1;
        return a.display_name.localeCompare(b.display_name);
      });
  }, [installedApps, search]);

  const toggleApp = (executable: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(executable)) {
        next.delete(executable);
      } else {
        next.add(executable);
      }
      return next;
    });
  };

  const handleSubmit = async () => {
    if (selected.size === 0) {
      setError("Select at least one application");
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      for (const exe of selected) {
        await axios.post(`${API_BASE}/add/`, { application: exe });
      }
      setSelected(new Set());
      setOpen(false);
      onApplicationAdded();
    } catch (err: any) {
      const msg = err.response?.data?.error || "Failed to add application";
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <button className="inline-flex items-center gap-2 px-3.5 py-2 text-[13px] font-medium text-foreground/70 bg-card hover:bg-secondary rounded-md transition-all cursor-pointer ring-1 ring-border/60 hover:ring-copper/30">
          <FaPlus size={9} className="text-copper/70" />
          Add Block
        </button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md bg-card border-border/60">
        <DialogHeader>
          <DialogTitle className="font-heading text-2xl text-foreground/95">
            Block application
          </DialogTitle>
          <DialogDescription className="text-muted-foreground text-sm">
            Select applications from your computer to block.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div>
            <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-2 block">
              Search applications
            </label>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter..."
              className="w-full bg-background ring-1 ring-border/60 rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/30 focus:outline-none focus:ring-copper/40 transition-all"
            />
          </div>
          <div className="max-h-60 overflow-y-auto rounded-md ring-1 ring-border/60 bg-background">
            {isLoading ? (
              <p className="text-sm text-muted-foreground text-center py-6">
                Loading applications...
              </p>
            ) : filtered.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-6">
                {installedApps.length === 0
                  ? "No applications found"
                  : "No matches"}
              </p>
            ) : (
              filtered.map((app) => {
                const isSelected = selected.has(app.executable);
                return (
                  <button
                    key={app.executable}
                    type="button"
                    onClick={() => toggleApp(app.executable)}
                    className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm text-left transition-colors ${
                      isSelected
                        ? "bg-copper/10 text-foreground"
                        : "text-foreground/70 hover:bg-secondary/50"
                    }`}
                  >
                    <div
                      className={`h-4 w-4 rounded border flex items-center justify-center shrink-0 transition-colors ${
                        isSelected
                          ? "bg-copper border-copper"
                          : "border-border/60"
                      }`}
                    >
                      {isSelected && (
                        <FaCheck size={8} className="text-copper-foreground" />
                      )}
                    </div>
                    <div className="flex flex-col min-w-0">
                      <span className="text-[13px] truncate">
                        {app.display_name}
                      </span>
                      <span className="font-mono text-[11px] text-muted-foreground/50 truncate">
                        {app.executable}
                      </span>
                    </div>
                  </button>
                );
              })
            )}
          </div>
          {error && (
            <p className="text-destructive text-xs">{error}</p>
          )}
        </div>
        <DialogFooter className="flex items-center justify-between sm:justify-between">
          <span className="text-xs font-mono text-muted-foreground/50">
            {selected.size} selected
          </span>
          <Button
            onClick={handleSubmit}
            disabled={isSubmitting || selected.size === 0}
            className="bg-copper text-copper-foreground hover:brightness-110"
          >
            {isSubmitting
              ? "Adding..."
              : `Block ${selected.size > 0 ? selected.size : ""} application${selected.size !== 1 ? "s" : ""}`}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
