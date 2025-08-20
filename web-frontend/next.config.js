/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/solve',
        destination: 'http://localhost:8000/api/solve', // Backend Python
      },
      {
        source: '/api/algorithms',
        destination: 'http://localhost:8000/algorithms',
      },
    ];
  },
}

module.exports = nextConfig
