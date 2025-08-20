/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    telemetry: false,
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'https://search-algorithms-applied-to-selfsolved.onrender.com',
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, PUT, DELETE, OPTIONS',
          },
          {
            key: 'Access-Control-Allow-Headers',
            value: 'Content-Type, Authorization',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig
