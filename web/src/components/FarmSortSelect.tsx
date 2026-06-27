"use client";

import { usePathname, useRouter } from "next/navigation";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { FARM_SORT_OPTIONS, type FarmSort } from "@/lib/farmFilters";

interface Props {
  sort: FarmSort;
  searchQuery: string;
  origin: string;
}

export function FarmSortSelect({ sort, searchQuery, origin }: Props) {
  const router = useRouter();
  const pathname = usePathname();

  function onChange(value: FarmSort) {
    const params = new URLSearchParams();
    if (searchQuery.trim()) params.set("q", searchQuery.trim());
    if (origin) params.set("origin", origin);
    if (value !== "asc") params.set("sort", value);
    params.set("page", "1");
    router.push(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-muted">Sort:</span>
      <Select value={sort} onValueChange={(v) => onChange(v as FarmSort)}>
        <SelectTrigger className="w-[130px]" aria-label="Sort farms">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {FARM_SORT_OPTIONS.map((opt) => (
            <SelectItem key={opt.value} value={opt.value}>
              {opt.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
