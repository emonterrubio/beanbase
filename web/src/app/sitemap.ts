import type { MetadataRoute } from "next";
import { api } from "@/lib/api";

const BASE = process.env.NEXT_PUBLIC_SITE_URL ?? "https://beanbase-theta.vercel.app";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const now = new Date();

  const [originsResult, ...farmPages] = await Promise.allSettled([
    api.origins.list(),
    api.farms.list({ page: 1, page_size: 100 }),
    api.farms.list({ page: 2, page_size: 100 }),
    api.farms.list({ page: 3, page_size: 100 }),
    api.farms.list({ page: 4, page_size: 100 }),
    api.farms.list({ page: 5, page_size: 100 }),
  ]);

  const staticRoutes: MetadataRoute.Sitemap = [
    { url: `${BASE}/`,         lastModified: now, changeFrequency: "weekly",  priority: 1.0 },
    { url: `${BASE}/farms`,    lastModified: now, changeFrequency: "daily",   priority: 0.9 },
    { url: `${BASE}/auctions`, lastModified: now, changeFrequency: "daily",   priority: 0.9 },
    { url: `${BASE}/origins`,  lastModified: now, changeFrequency: "weekly",  priority: 0.8 },
  ];

  const originRoutes: MetadataRoute.Sitemap =
    originsResult.status === "fulfilled"
      ? originsResult.value
          .filter((o) => !o.region)
          .map((o) => ({
            url: `${BASE}/origins/${encodeURIComponent(o.country)}`,
            lastModified: now,
            changeFrequency: "monthly" as const,
            priority: 0.7,
          }))
      : [];

  const farmRoutes: MetadataRoute.Sitemap = farmPages
    .flatMap((r) => (r.status === "fulfilled" ? r.value.items : []))
    .map((f) => ({
      url: `${BASE}/farms/${f.slug}`,
      lastModified: now,
      changeFrequency: "monthly" as const,
      priority: 0.6,
    }));

  return [...staticRoutes, ...originRoutes, ...farmRoutes];
}
