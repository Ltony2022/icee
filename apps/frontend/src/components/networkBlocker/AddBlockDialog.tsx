import { useState } from "react";
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
import { FaPlus } from "react-icons/fa";
import { getBackendOrigin } from "@/config/backendOrigin";

interface AddBlockDialogProps {
  onDomainAdded: () => void;
}

export function AddBlockDialog({ onDomainAdded }: AddBlockDialogProps) {
  const [domain, setDomain] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);

  const handleSubmit = async () => {
    const trimmed = domain.trim().toLowerCase();
    if (!trimmed) {
      setError("Domain is required");
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      await axios.post(`${getBackendOrigin()}/api/dns-proxy/blocked-domains/add/`, {
        domain: trimmed,
      });
      setDomain("");
      setOpen(false);
      onDomainAdded();
    } catch (err: any) {
      const msg = err.response?.data?.error || "Failed to add domain";
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSubmit();
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
            Block website
          </DialogTitle>
          <DialogDescription className="text-muted-foreground text-sm">
            Add a domain to block via DNS proxy. Subdomains are automatically blocked.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div>
            <label className="text-[10px] font-mono font-medium text-muted-foreground/50 uppercase tracking-[0.15em] mb-2 block">
              Domain
            </label>
            <input
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="example.com"
              className="w-full bg-background ring-1 ring-border/60 rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/30 focus:outline-none focus:ring-copper/40 transition-all"
            />
            {error && (
              <p className="text-destructive text-xs mt-2">{error}</p>
            )}
          </div>
        </div>
        <DialogFooter>
          <Button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="bg-copper text-copper-foreground hover:brightness-110"
          >
            {isSubmitting ? "Adding..." : "Block domain"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
