import Link from "next/link";
import * as React from "react";
import { ChevronLeftIcon, ChevronRightIcon, MoreHorizontalIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";

function Pagination({ className, ...props }: React.ComponentProps<"nav">) {
  return (
    <nav
      role="navigation"
      aria-label="pagination"
      className={cn("mx-auto flex w-full justify-center", className)}
      {...props}
    />
  );
}

function PaginationContent({ className, ...props }: React.ComponentProps<"ul">) {
  return (
    <ul
      className={cn("flex flex-row items-center gap-1", className)}
      {...props}
    />
  );
}

function PaginationItem({ ...props }: React.ComponentProps<"li">) {
  return <li {...props} />;
}

type PaginationLinkProps = {
  isActive?: boolean;
} & React.ComponentProps<typeof Link>;

function PaginationLink({
  className,
  isActive,
  ...props
}: PaginationLinkProps) {
  return (
    <Link
      aria-current={isActive ? "page" : undefined}
      className={cn(
        buttonVariants({
          variant: isActive ? "default" : "outline",
          size: "icon",
        }),
        "h-9 w-9",
        className,
      )}
      {...props}
    />
  );
}

function PaginationPrevious({
  className,
  text = "Previous",
  ...props
}: PaginationLinkProps & { text?: string }) {
  return (
    <Link
      aria-label="Go to previous page"
      className={cn(
        buttonVariants({ variant: "outline", size: "default" }),
        "gap-1 px-2.5 sm:pl-2.5",
        className,
      )}
      {...props}
    >
      <ChevronLeftIcon className="h-4 w-4" />
      <span className="hidden sm:block">{text}</span>
    </Link>
  );
}

function PaginationNext({
  className,
  text = "Next",
  ...props
}: PaginationLinkProps & { text?: string }) {
  return (
    <Link
      aria-label="Go to next page"
      className={cn(
        buttonVariants({ variant: "outline", size: "default" }),
        "gap-1 px-2.5 sm:pr-2.5",
        className,
      )}
      {...props}
    >
      <span className="hidden sm:block">{text}</span>
      <ChevronRightIcon className="h-4 w-4" />
    </Link>
  );
}

function PaginationEllipsis({ className, ...props }: React.ComponentProps<"span">) {
  return (
    <span
      aria-hidden
      className={cn("flex h-9 w-9 items-center justify-center", className)}
      {...props}
    >
      <MoreHorizontalIcon className="h-4 w-4 text-muted" />
      <span className="sr-only">More pages</span>
    </span>
  );
}

export {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
};
