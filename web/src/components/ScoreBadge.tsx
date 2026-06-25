interface Props {
  score: number | null;
  size?: "sm" | "md";
}

function tier(score: number): { label: string; className: string } {
  if (score >= 90) return { label: "Exceptional", className: "bg-score-exceptional text-white" };
  if (score >= 87) return { label: "Outstanding", className: "bg-score-outstanding text-white" };
  if (score >= 84) return { label: "Excellent",   className: "bg-score-excellent text-white" };
  return { label: "", className: "bg-fog-100 text-fog-600" };
}

export function ScoreBadge({ score, size = "md" }: Props) {
  if (score == null) return null;
  const { className } = tier(score);
  const padding = size === "sm" ? "px-2 py-0.5 text-xs" : "px-2.5 py-1 text-sm";
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-badge font-semibold tabular-nums ${padding} ${className}`}>
      {score.toFixed(2)}
    </span>
  );
}
