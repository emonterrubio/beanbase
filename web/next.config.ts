import type { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig: NextConfig = {};

export default withSentryConfig(nextConfig, {
  silent: true,
  disableLogger: true,
  // Source map upload requires SENTRY_AUTH_TOKEN — skip for now
  sourcemaps: { disable: true },
});
