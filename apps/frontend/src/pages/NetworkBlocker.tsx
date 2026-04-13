import { useState, useEffect, useMemo, useCallback } from "react";
import axios from "axios";

import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
} from "@tanstack/react-table";
import { ArrowUpDown, Trash2, Power, PowerOff } from "lucide-react";

import { AddBlockDialog } from "@/components/networkBlocker/AddBlockDialog.tsx";
import { Button } from "@/components/ui/button.tsx";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input.tsx";
import type { ProxyStatus } from "@/types/networkBlocker";
import { getBackendOrigin } from "@/config/backendOrigin";

interface BlockedDomainRow {
  domain: string;
}

const API_BASE = `${getBackendOrigin()}/api/dns-proxy`;

export default function NetworkBlocker() {
  const [domains, setDomains] = useState<BlockedDomainRow[]>([]);
  const [proxyStatus, setProxyStatus] = useState<ProxyStatus>({
    running: false,
  });
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [isToggling, setIsToggling] = useState(false);

  const fetchDomains = useCallback(async () => {
    try {
      const res = await axios.get(`${API_BASE}/blocked-domains/`);
      const list: string[] = res.data.blocked_domains ?? [];
      setDomains(list.map((d) => ({ domain: d })));
    } catch {
      // backend may not be running yet
    }
  }, []);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await axios.get(`${API_BASE}/status/`);
      setProxyStatus(res.data);
    } catch {
      setProxyStatus({ running: false });
    }
  }, []);

  useEffect(() => {
    fetchDomains();
    fetchStatus();
  }, [fetchDomains, fetchStatus]);

  const handleDelete = async (domain: string) => {
    try {
      await axios.delete(`${API_BASE}/blocked-domains/remove/`, {
        data: { domain },
      });
      fetchDomains();
    } catch (err) {
      console.error("Failed to remove domain:", err);
    }
  };

  const handleToggleProxy = async () => {
    setIsToggling(true);
    try {
      if (proxyStatus.running) {
        await axios.post(`${API_BASE}/stop/`);
      } else {
        await axios.post(`${API_BASE}/start/`);
      }
      await fetchStatus();
    } catch (err) {
      console.error("Failed to toggle proxy:", err);
    } finally {
      setIsToggling(false);
    }
  };

  const columns = useMemo<ColumnDef<BlockedDomainRow>[]>(
    () => [
      {
        accessorKey: "domain",
        header: ({ column }) => (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
            className="hover:bg-secondary text-muted-foreground hover:text-foreground/80 -ml-4 text-xs"
          >
            Domain
            <ArrowUpDown className="ml-2 h-3 w-3" />
          </Button>
        ),
        cell: ({ row }) => (
          <span className="font-mono text-sm text-foreground/80">
            {row.getValue("domain")}
          </span>
        ),
      },
      {
        id: "method",
        header: () => (
          <span className="text-xs text-muted-foreground">Method</span>
        ),
        cell: () => (
          <span className="px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-sage/10 text-sage ring-1 ring-sage/20">
            DNS
          </span>
        ),
      },
      {
        id: "scope",
        header: () => (
          <span className="text-xs text-muted-foreground">Scope</span>
        ),
        cell: () => (
          <span className="text-sm text-muted-foreground">+ subdomains</span>
        ),
      },
      {
        id: "actions",
        header: () => (
          <div className="text-right text-xs text-muted-foreground">
            Actions
          </div>
        ),
        cell: ({ row }) => (
          <div className="flex justify-end gap-1.5">
            <button
              onClick={() => handleDelete(row.original.domain)}
              className="p-1.5 rounded-md text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
              title="Remove"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </button>
          </div>
        ),
      },
    ],
    [],
  );

  const table = useReactTable({
    data: domains,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    state: { sorting, globalFilter },
    initialState: { pagination: { pageSize: 10 } },
  });

  return (
    <div className="w-full h-full flex flex-col px-10 py-10 mx-auto max-w-4xl">
      {/* Header */}
      <div className="mb-10 flex justify-between items-start animate-fade-up">
        <div>
          <h1 className="font-heading text-4xl text-foreground/95 tracking-tight">
            Network <span className="italic text-copper">Blocker</span>
          </h1>
          <p className="text-muted-foreground mt-1.5 text-sm">
            Block websites via DNS proxy. Manage blocked domains and proxy
            status.
          </p>
        </div>
        <AddBlockDialog onDomainAdded={fetchDomains} />
      </div>

      {/* Proxy status bar */}
      <div
        className="flex items-center justify-between rounded-lg bg-card ring-1 ring-border/60 px-5 py-3.5 mb-5 animate-fade-up"
        style={{ animationDelay: "60ms" }}
      >
        <div className="flex items-center gap-3">
          <div
            className={`h-2 w-2 rounded-full ${
              proxyStatus.running
                ? "bg-sage animate-pulse"
                : "bg-muted-foreground/30"
            }`}
          />
          <span className="text-sm text-foreground/80">
            DNS Proxy{" "}
            <span className="font-mono text-xs text-muted-foreground">
              {proxyStatus.running
                ? `running (PID ${proxyStatus.pid})`
                : "stopped"}
            </span>
          </span>
        </div>
        <button
          onClick={handleToggleProxy}
          disabled={isToggling}
          className={`inline-flex items-center gap-2 px-3.5 py-2 text-[13px] font-medium rounded-md transition-all cursor-pointer ring-1 ${
            proxyStatus.running
              ? "text-destructive/80 bg-destructive/5 ring-destructive/20 hover:bg-destructive/10"
              : "text-sage bg-sage/5 ring-sage/20 hover:bg-sage/10"
          } disabled:opacity-50`}
        >
          {proxyStatus.running ? (
            <>
              <PowerOff className="h-3.5 w-3.5" />
              {isToggling ? "Stopping..." : "Stop"}
            </>
          ) : (
            <>
              <Power className="h-3.5 w-3.5" />
              {isToggling ? "Starting..." : "Start"}
            </>
          )}
        </button>
      </div>

      {/* Search */}
      <div
        className="flex gap-3 mb-5 animate-fade-up"
        style={{ animationDelay: "80ms" }}
      >
        <Input
          placeholder="Search domains..."
          value={globalFilter ?? ""}
          onChange={(e) => setGlobalFilter(e.target.value)}
          className="max-w-xs bg-card ring-1 ring-border/60 border-0 text-sm placeholder:text-muted-foreground/40 focus-visible:ring-copper/40"
        />
      </div>

      {/* Table */}
      <div
        className="rounded-lg bg-card ring-1 ring-border/60 overflow-hidden noise animate-fade-up"
        style={{ animationDelay: "140ms" }}
      >
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow
                key={headerGroup.id}
                className="border-border/40 hover:bg-transparent"
              >
                {headerGroup.headers.map((header) => (
                  <TableHead
                    key={header.id}
                    className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 pl-5"
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  className="border-border/30 transition-colors hover:bg-secondary/40"
                >
                  {row.getVisibleCells().map((cell, index) => (
                    <TableCell
                      key={cell.id}
                      className={index === 0 ? "pl-5" : ""}
                    >
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center text-muted-foreground text-sm"
                >
                  No blocked domains. Add one to get started.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between py-4">
        <p className="text-xs font-mono text-muted-foreground/50">
          {table.getFilteredRowModel().rows.length} domain(s) blocked
        </p>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            className="text-xs bg-card"
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            className="text-xs bg-card"
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
