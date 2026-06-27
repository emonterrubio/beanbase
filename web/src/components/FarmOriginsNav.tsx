"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

function buildOriginUrl(
  pathname: string,
  origin: string,
  searchQuery: string,
  sort: string,
): string {
  const params = new URLSearchParams();
  if (searchQuery.trim()) params.set("q", searchQuery.trim());
  if (origin) params.set("origin", origin);
  if (sort && sort !== "asc") params.set("sort", sort);
  params.set("page", "1");
  const qs = params.toString();
  return qs ? `${pathname}?${qs}` : pathname;
}

function navLinkClass(active: boolean): string {
  const base =
    "group flex rounded-md px-3 py-2 text-sm font-medium transition-colors";
  if (active) {
    return `${base} bg-cream-100 text-brand`;
  }
  return `${base} text-text hover:bg-cream-50 hover:text-brand`;
}

interface Props {
  origins: string[];
  selectedOrigin: string;
  searchQuery: string;
  sort: string;
}

export function FarmOriginsNav({
  origins,
  selectedOrigin,
  searchQuery,
  sort,
}: Props) {
  const pathname = usePathname();
  const allHref = buildOriginUrl(pathname, "", searchQuery, sort);

  return (
    <nav aria-label="Origins" className="rounded-card border border-border bg-white">
      <div className="border-b border-border px-4 py-3">
        <h2 className="text-sm font-semibold text-text">Origins</h2>
      </div>

      <ul role="list" className="max-h-[calc(100vh-10rem)] overflow-y-auto p-2">
        <li>
          <Link href={allHref} className={navLinkClass(!selectedOrigin)}>
            All farms
          </Link>
        </li>
        {origins.map((country) => {
          const active =
            selectedOrigin.toLowerCase() === country.toLowerCase();
          return (
            <li key={country}>
              <Link
                href={buildOriginUrl(pathname, country, searchQuery, sort)}
                className={navLinkClass(active)}
                aria-current={active ? "page" : undefined}
              >
                {country}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
