import Link from "next/link";
import type { LotRow } from "@/lib/api";
import { ScoreBadge } from "./ScoreBadge";

function fmt(n: number | null | undefined, decimals = 2, prefix = "") {
  if (n == null) return "—";
  return `${prefix}${n.toFixed(decimals)}`;
}

export function LotTable({ lots }: { lots: LotRow[] }) {
  if (lots.length === 0) {
    return (
      <p className="py-12 text-center text-sm text-muted">
        No auction lots found.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-card border border-border">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border bg-cream-50 text-xs uppercase tracking-wide text-muted">
            <th className="px-4 py-3 text-left">Rank</th>
            <th className="px-4 py-3 text-left">Farm</th>
            <th className="px-4 py-3 text-left">Country</th>
            <th className="px-4 py-3 text-left">Year</th>
            <th className="px-4 py-3 text-left">Score</th>
            <th className="px-4 py-3 text-left">Process</th>
            <th className="px-4 py-3 text-right">$/kg</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {lots.map((lot) => (
            <tr key={lot.id} className="group bg-white transition-colors hover:bg-cream-50">
              <td className="px-4 py-3 font-mono text-xs text-muted">{lot.lot_rank ?? "—"}</td>
              <td className="px-4 py-3 font-medium text-text">
                {lot.farm_id ? (
                  <Link
                    href={`/farms/${lot.farm_id}`}
                    className="hover:text-brand hover:underline"
                  >
                    {lot.farm_name ?? "Unknown"}
                  </Link>
                ) : (
                  lot.farm_name ?? "—"
                )}
              </td>
              <td className="px-4 py-3 text-muted">{lot.country ?? "—"}</td>
              <td className="px-4 py-3 tabular-nums text-muted">{lot.year ?? "—"}</td>
              <td className="px-4 py-3">
                <ScoreBadge score={lot.score} size="sm" />
              </td>
              <td className="px-4 py-3 text-muted">{lot.process_method ?? "—"}</td>
              <td className="px-4 py-3 text-right tabular-nums text-muted">
                {fmt(lot.winning_price_usd_per_kg, 2, "$")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
