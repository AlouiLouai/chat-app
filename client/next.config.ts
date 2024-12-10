import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  outputFileTracingExcludes: {
    "*": ["__nextjs_original-stack-frame"],
  },
};

export default nextConfig;
