const CERT_COLORS: Record<string, string> = {
  "Rainforest Alliance": "bg-green-100 text-green-800 border-green-200",
  "Fair Trade":          "bg-blue-100 text-blue-800 border-blue-200",
  "Organic":             "bg-lime-100 text-lime-800 border-lime-200",
  "UTZ":                 "bg-teal-100 text-teal-800 border-teal-200",
};

export function CertBadge({ cert }: { cert: string }) {
  const colors = CERT_COLORS[cert] ?? "bg-fog-100 text-fog-700 border-fog-200";
  return (
    <span className={`inline-flex items-center rounded-badge border px-2 py-0.5 text-xs font-medium ${colors}`}>
      {cert}
    </span>
  );
}
