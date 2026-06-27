"use client";

import { SlidersHorizontal } from "lucide-react";
import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { formatSourceLabel } from "@/lib/farmFilters";

interface DraftFilters {
  origin: string;
  source: string;
  process: string;
}

interface Props {
  availableOrigins: string[];
  availableSources: string[];
  availableProcesses: string[];
  origin: string;
  source: string;
  process: string;
  searchQuery: string;
  sort: string;
}

function buildUrl(
  pathname: string,
  draft: DraftFilters,
  searchQuery: string,
  sort: string,
): string {
  const params = new URLSearchParams();
  if (searchQuery.trim()) params.set("q", searchQuery.trim());
  if (draft.origin) params.set("origin", draft.origin);
  if (draft.source) params.set("source", draft.source);
  if (draft.process) params.set("process", draft.process);
  if (sort && sort !== "asc") params.set("sort", sort);
  params.set("page", "1");
  const qs = params.toString();
  return qs ? `${pathname}?${qs}` : pathname;
}

export function FarmFilterSidebar({
  availableOrigins,
  availableSources,
  availableProcesses,
  origin,
  source,
  process,
  searchQuery,
  sort,
}: Props) {
  const router = useRouter();
  const pathname = usePathname();
  const [draft, setDraft] = useState<DraftFilters>({ origin, source, process });

  useEffect(() => {
    setDraft({ origin, source, process });
  }, [origin, source, process]);

  function apply() {
    router.push(buildUrl(pathname, draft, searchQuery, sort));
  }

  function clearAll() {
    const empty = { origin: "", source: "", process: "" };
    setDraft(empty);
    router.push(buildUrl(pathname, empty, searchQuery, sort));
  }

  function toggleOrigin(value: string) {
    setDraft((prev) => ({
      ...prev,
      origin: prev.origin === value ? "" : value,
    }));
  }

  const hasFilters =
    Boolean(origin || source || process) ||
    Boolean(draft.origin || draft.source || draft.process);

  return (
    <aside className="rounded-card border border-border bg-white">
      <div className="flex items-center gap-2 border-b border-border px-4 py-3">
        <SlidersHorizontal className="h-4 w-4 text-muted" aria-hidden />
        <h2 className="text-sm font-semibold text-text">Filters</h2>
      </div>

      <div className="max-h-[calc(100vh-12rem)] overflow-y-auto p-4">
        {/* Origin */}
        <fieldset className="border-b border-border pb-4">
          <legend className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted">
            Origin
          </legend>
          {availableOrigins.length === 0 ? (
            <p className="text-xs text-muted">No origins match current filters.</p>
          ) : (
            <ul className="max-h-48 space-y-2 overflow-y-auto pr-1">
              {availableOrigins.map((o) => (
                <li key={o}>
                  <label className="flex cursor-pointer items-center gap-2.5 text-sm text-text">
                    <input
                      type="checkbox"
                      checked={draft.origin === o}
                      onChange={() => toggleOrigin(o)}
                      className="h-4 w-4 rounded border-border text-brand focus:ring-brand"
                    />
                    {o}
                  </label>
                </li>
              ))}
            </ul>
          )}
        </fieldset>

        {/* Source */}
        <div className="border-b border-border py-4">
          <label
            htmlFor="farm-source-filter"
            className="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted"
          >
            Source
          </label>
          <Select
            value={draft.source || "all"}
            onValueChange={(v) =>
              setDraft((prev) => ({ ...prev, source: v === "all" ? "" : v }))
            }
            disabled={availableSources.length === 0}
          >
            <SelectTrigger id="farm-source-filter" className="w-full">
              <SelectValue placeholder="All sources" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All sources</SelectItem>
              {availableSources.map((s) => (
                <SelectItem key={s} value={s}>
                  {formatSourceLabel(s)}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Process */}
        <div className="pt-4">
          <label
            htmlFor="farm-process-filter"
            className="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted"
          >
            Process method
          </label>
          <Select
            value={draft.process || "all"}
            onValueChange={(v) =>
              setDraft((prev) => ({ ...prev, process: v === "all" ? "" : v }))
            }
            disabled={availableProcesses.length === 0}
          >
            <SelectTrigger id="farm-process-filter" className="w-full">
              <SelectValue placeholder="All processes" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All processes</SelectItem>
              {availableProcesses.map((p) => (
                <SelectItem key={p} value={p}>
                  {p}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-2 border-t border-border p-4">
        <Button type="button" className="w-full" onClick={apply}>
          Apply filters
        </Button>
        {hasFilters && (
          <button
            type="button"
            onClick={clearAll}
            className="w-full text-center text-xs text-muted transition-colors hover:text-brand"
          >
            Clear all filters
          </button>
        )}
      </div>
    </aside>
  );
}
