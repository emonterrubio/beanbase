"use client";

import { usePathname, useRouter } from "next/navigation";
import { useRef } from "react";

interface Props {
  placeholder?: string;
  defaultValue?: string;
  paramKey?: string;
  currentParams?: Record<string, string>;
}

export function SearchBar({
  placeholder = "Search…",
  defaultValue = "",
  paramKey = "q",
  currentParams = {},
}: Props) {
  const router = useRouter();
  const pathname = usePathname();
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (timer.current) clearTimeout(timer.current);
    const val = e.target.value;
    timer.current = setTimeout(() => {
      const params = new URLSearchParams();
      for (const [k, v] of Object.entries(currentParams)) {
        if (k !== paramKey) params.set(k, v);
      }
      params.set("page", "1");
      if (val.trim()) params.set(paramKey, val.trim());
      router.push(`${pathname}?${params.toString()}`);
    }, 350);
  }

  return (
    <div className="relative">
      <svg
        className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1 0 6.5 6.5a7.5 7.5 0 0 0 10.15 10.15z"
        />
      </svg>
      <input
        type="search"
        defaultValue={defaultValue}
        onChange={handleChange}
        placeholder={placeholder}
        className="w-full rounded-card border border-border bg-white py-2 pl-9 pr-4 text-sm text-text placeholder:text-muted focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
      />
    </div>
  );
}
