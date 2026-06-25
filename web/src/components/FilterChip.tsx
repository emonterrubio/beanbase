"use client";

import { usePathname, useRouter } from "next/navigation";

interface Props {
  label: string;
  param: string;
  value: string;
  isActive: boolean;
  currentParams?: Record<string, string>;
}

export function FilterChip({
  label,
  param,
  value,
  isActive,
  currentParams = {},
}: Props) {
  const router = useRouter();
  const pathname = usePathname();

  function handleClick() {
    const params = new URLSearchParams(currentParams);
    params.set("page", "1");
    if (isActive) {
      params.delete(param);
    } else {
      params.set(param, value);
    }
    router.push(`${pathname}?${params.toString()}`);
  }

  return (
    <button
      onClick={handleClick}
      className={[
        "rounded-badge border px-3 py-1 text-xs font-medium transition-colors",
        isActive
          ? "border-brand bg-brand text-white"
          : "border-border bg-white text-muted hover:border-brand hover:text-brand",
      ].join(" ")}
    >
      {label}
    </button>
  );
}
