import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { getPaginationRange } from "@/lib/farmFilters";

interface Props {
  page: number;
  pages: number;
  hrefBase: string;
}

export function FarmPagination({ page, pages, hrefBase }: Props) {
  if (pages <= 1) return null;

  const prev = page > 1 ? `${hrefBase}page=${page - 1}` : undefined;
  const next = page < pages ? `${hrefBase}page=${page + 1}` : undefined;
  const range = getPaginationRange(page, pages);

  return (
    <Pagination className="py-6">
      <PaginationContent>
        <PaginationItem>
          {prev ? (
            <PaginationPrevious href={prev} />
          ) : (
            <span
              aria-disabled
              className="inline-flex h-9 cursor-not-allowed items-center gap-1 px-2.5 text-sm text-fog-300 sm:pl-2.5"
            >
              Previous
            </span>
          )}
        </PaginationItem>

        {range.map((item, idx) =>
          item === "ellipsis" ? (
            <PaginationItem key={`ellipsis-${idx}`}>
              <PaginationEllipsis />
            </PaginationItem>
          ) : (
            <PaginationItem key={item}>
              <PaginationLink href={`${hrefBase}page=${item}`} isActive={item === page}>
                {item}
              </PaginationLink>
            </PaginationItem>
          ),
        )}

        <PaginationItem>
          {next ? (
            <PaginationNext href={next} />
          ) : (
            <span
              aria-disabled
              className="inline-flex h-9 cursor-not-allowed items-center gap-1 px-2.5 text-sm text-fog-300 sm:pr-2.5"
            >
              Next
            </span>
          )}
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
}
