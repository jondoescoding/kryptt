/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config: any, { isServer }: { isServer: boolean }) => {
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
  poweredByHeader: false,
  // Add production specific settings
  distDir: '.next',
  reactStrictMode: true,
  swcMinify: true,
  // Handle 404s properly
  async rewrites() {
    return {
      fallback: [
        {
          source: '/:path*',
          destination: '/_not-found'
        }
      ]
    }
  },
  // Ensure static files are copied to the standalone build
  experimental: {
    outputFileTracingRoot: process.env.NODE_ENV === "production" ? "./" : undefined,
    outputFileTracingExcludes: {
      '*': [
        'node_modules/@swc/core-linux-x64-gnu',
        'node_modules/@swc/core-linux-x64-musl',
        'node_modules/@esbuild/linux-x64',
      ],
    },
  }
};

module.exports = nextConfig;
