import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    // Ignore punycode warning
    config.ignoreWarnings = [
      { module: /node_modules\/punycode/ }
    ];
    return config;
  },
  output: 'standalone',
  // Enable static compression
  compress: true,
  // Add trailing slash handling
  trailingSlash: false,
  // Disable powered by header
  poweredByHeader: false
};

export default nextConfig;
