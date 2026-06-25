import Link from "next/link";

interface Props {
  page: number;
  pages: number;
  /** Base href ending with "?" or "&", ready to append page=N */
  hrefBase: string;
}

export function Pagination({ page, pages, hrefBase }: Props) {
  if (pages <= 1) return null;

  const prev = page > 1 ? `${hrefBase}page=${page - 1}` : null;
  const next = page < pages ? `${hrefBase}page=${page + 1}` : null;

  return (
    <nav
      aria-label="Pagination"
      className="flex items-center justify-center gap-2 py-6 text-sm"
    >
      {prev ? (
        <Link
          href={prev}
          className="rounded-card border border-border bg-white px-4 py-2 text-muted transition-colors hover:border-brand hover:text-brand"
        >
          ← Previous
        </Link>
      ) : (
        <span className="rounded-card border border-border px-4 py-2 text-fog-300 cursor-not-allowed">
          ← Previous
        </span>
      )}

      <span className="px-3 text-muted">
        {page} / {pages}
      </span>

      {next ? (
        <Link
          href={next}
          className="rounded-card border border-border bg-white px-4 py-2 text-muted transition-colors hover:border-brand hover:text-brand"
        >
          Next →
        </Link>
      ) : (
        <span className="rounded-card border border-border px-4 py-2 text-fog-300 cursor-not-allowed">
          Next →
        </span>
      )}
    </nav>
  );
}
