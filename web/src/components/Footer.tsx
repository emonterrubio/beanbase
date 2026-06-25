import Link from "next/link";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-border bg-white">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="flex flex-col items-start justify-between gap-8 sm:flex-row sm:items-center">
          <div className="flex flex-col gap-1">
            <Link href="/" className="flex items-center gap-2 text-base font-bold text-brand">
              <span className="inline-block h-5 w-5 rounded-full bg-honey-500" aria-hidden />
              BeanBase
            </Link>
            <p className="text-xs text-muted">
              The global intelligence layer for specialty coffee.
            </p>
          </div>

          <nav className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-muted">
            <Link href="/farms"    className="hover:text-text">Farms</Link>
            <Link href="/auctions" className="hover:text-text">Auctions</Link>
            <Link href="/origins"  className="hover:text-text">Origins</Link>
            <Link href="/docs"     className="hover:text-text">API Docs</Link>
          </nav>
        </div>

        <p className="mt-8 text-xs text-fog-400">
          © {new Date().getFullYear()} BeanBase. Data sourced from Cup of Excellence and public auction records.
        </p>
      </div>
    </footer>
  );
}
