/** Country display name — uses API value, or derives from slug prefix (e.g. nicaragua--farm). */
export function resolveFarmCountry(farm: {
  country: string | null;
  slug: string;
}): string | null {
  if (farm.country) return farm.country;
  const prefix = farm.slug.split("--")[0];
  if (!prefix) return null;
  return prefix
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
