/** @type {import('next').NextConfig} */
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

const config = {
  async rewrites() {
    return [
      {
        source: "/api/health",
        destination: `${backendUrl}/health`
      }
    ];
  }
};

export default config;
