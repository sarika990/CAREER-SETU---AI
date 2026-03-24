/** @type {import('next').NextConfig} */
const nextConfig = {
    swcMinify: false, // Reduce memory usage during dev
    async rewrites() {
        // Only apply the local dev proxy when NEXT_PUBLIC_API_URL is NOT set
        // (i.e. running locally where Next.js proxies to localhost:8000)
        // Disable local proxy rewrites in production/Render environment
        if (process.env.NEXT_PUBLIC_API_URL || process.env.NODE_ENV === 'production' || process.env.RENDER === 'true') {
            return [];
        }
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8000/api/:path*',
            },
            {
                source: '/uploads/:path*',
                destination: 'http://localhost:8000/uploads/:path*',
            },
        ];
    },
};

export default nextConfig;
