import Image from "next/image";
import { countryImageUrl } from "@/lib/countryImages";

type CountryBannerProps = {
  country: string | null | undefined;
  /** card = farm grid thumbnail; banner = farm detail hero */
  variant?: "card" | "banner";
  priority?: boolean;
};

const SIZES = {
  card: { width: 640, height: 360, className: "aspect-[16/10] w-full" },
  banner: { width: 1400, height: 420, className: "h-48 w-full sm:h-64 md:h-72" },
} as const;

export function CountryBanner({
  country,
  variant = "card",
  priority = false,
}: CountryBannerProps) {
  const { width, height, className } = SIZES[variant];
  const label = country ?? "Coffee origin";

  return (
    <div className={`relative overflow-hidden bg-cream-100 ${className}`}>
      <Image
        src={countryImageUrl(country, width)}
        alt={`${label} landscape`}
        fill
        sizes={variant === "banner" ? "100vw" : "(max-width: 640px) 100vw, 320px"}
        className="object-cover transition-transform duration-300 group-hover:scale-105"
        priority={priority}
      />
      <div
        className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/25 to-transparent"
        aria-hidden
      />
    </div>
  );
}
