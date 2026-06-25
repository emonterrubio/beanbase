import type { Metadata } from "next";
import { api } from "@/lib/api";
import { OriginCard } from "@/components/OriginCard";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Origins" };

export default async function OriginsPage() {
  const origins = await api.origins.list();
  // Show country-level rows first (region == null)
  const countries = origins.filter((o) => !o.region);
  const regions   = origins.filter((o) =>  o.region);

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-text">Origins</h1>
        <p className="mt-1 text-sm text-muted">
          {countries.length} producing countries with altitude, harvest, and flavor data
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {countries.map((origin) => (
          <OriginCard key={origin.id} origin={origin} />
        ))}
      </div>

      {regions.length > 0 && (
        <>
          <h2 className="mb-4 mt-12 text-lg font-semibold text-text">Regions</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {regions.map((origin) => (
              <OriginCard key={origin.id} origin={origin} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
