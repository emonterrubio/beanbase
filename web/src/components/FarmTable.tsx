import Link from "next/link";
import type { FarmSummary } from "@/lib/api";
import { farmCell, displayProcess, displayVarietal } from "@/lib/farmDisplay";

export function FarmTable({ farms }: { farms: FarmSummary[] }) {
  if (farms.length === 0) {
    return (
      <p className="py-12 text-center text-sm text-muted">
        No farms found. Try adjusting your filters.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-card border border-border">
      <table className="w-full min-w-[64rem] text-sm">
        <thead>
          <tr className="border-b border-border bg-cream-50 text-xs uppercase tracking-wide text-muted">
            <th className="px-3 py-3 text-left">Producer / Micro-Region</th>
            <th className="px-3 py-3 text-left">Farm</th>
            <th className="px-3 py-3 text-left">Municipality</th>
            <th className="px-3 py-3 text-left">Department</th>
            <th className="px-3 py-3 text-left">Varietal</th>
            <th className="px-3 py-3 text-left">Process</th>
            <th className="px-3 py-3 text-left">Packaging</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {farms.map((farm) => (
            <tr
              key={farm.id}
              className="group bg-white transition-colors hover:bg-cream-50"
            >
              <td className="max-w-[10rem] px-3 py-3 text-muted">
                <span className="line-clamp-2">{farmCell(farm.owner_name)}</span>
              </td>
              <td className="max-w-xs px-3 py-3 font-medium text-text">
                <Link
                  href={`/farms/${farm.slug}`}
                  className="line-clamp-2 hover:text-brand hover:underline"
                >
                  {farm.canonical_name}
                </Link>
              </td>
              <td className="whitespace-nowrap px-3 py-3 text-muted">
                {farmCell(farm.municipality)}
              </td>
              <td className="whitespace-nowrap px-3 py-3 text-muted">
                {farmCell(farm.department)}
              </td>
              <td className="max-w-[10rem] px-3 py-3 text-muted">
                <span className="line-clamp-2">{displayVarietal(farm)}</span>
              </td>
              <td className="max-w-[10rem] px-3 py-3 text-muted">
                <span className="line-clamp-2">{displayProcess(farm)}</span>
              </td>
              <td className="whitespace-nowrap px-3 py-3 text-muted">
                {farmCell(farm.packaging_type)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
