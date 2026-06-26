import Link from "next/link";
import { UserButton } from "@clerk/nextjs";
import { auth } from "@clerk/nextjs/server";

const LINKS = [
  { href: "/farms",    label: "Farms"    },
  { href: "/auctions", label: "Auctions" },
  { href: "/origins",  label: "Origins"  },
];

export async function Nav() {
  const { userId } = await auth();

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2 text-lg font-bold tracking-tight text-brand"
        >
          <span className="inline-block h-6 w-6 rounded-full bg-honey-500" aria-hidden />
          BeanBase
        </Link>

        <nav className="flex items-center gap-6">
          {LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className="hidden text-sm font-medium text-muted transition-colors hover:text-text sm:block"
            >
              {label}
            </Link>
          ))}

          {userId ? (
            <>
              <Link
                href="/dashboard"
                className="hidden text-sm font-medium text-muted transition-colors hover:text-text sm:block"
              >
                Dashboard
              </Link>
              <UserButton />
            </>
          ) : (
            <>
              <Link
                href="/sign-in"
                className="hidden text-sm font-medium text-muted transition-colors hover:text-text sm:block"
              >
                Sign in
              </Link>
              <Link
                href="/sign-up"
                className="rounded-badge bg-brand px-4 py-1.5 text-sm font-medium text-white transition-colors hover:bg-bean-brown-700"
              >
                Sign up free
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
