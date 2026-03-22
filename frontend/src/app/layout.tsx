import type { Metadata } from "next";
import "./globals.css";
import { NotificationProvider } from "@/components/NotificationProvider";
import { GlobalVoiceAssistant } from "@/components/GlobalVoiceAssistant";
export const metadata: Metadata = {
    title: "Career Setu AI — Intelligent Career & Upskilling Platform",
    description:
        "AI-powered career guidance and skill development platform. Identify skill gaps, get personalized learning roadmaps, and connect with real job opportunities across India.",
    keywords: "career guidance, skill development, AI, upskilling, jobs, India, Career Setu",
};

import PageTransition from "@/components/PageTransition";

export default function RootLayout({
    children,
}: Readonly<{ children: React.ReactNode }>) {
    return (
        <html lang="en" className="dark">
            <body className="bg-dark-950 text-dark-200 antialiased bg-grid min-h-screen relative overflow-x-hidden">
                <NotificationProvider>
                    <PageTransition>
                        {children}
                    </PageTransition>
                    <GlobalVoiceAssistant />
                </NotificationProvider>
            </body>
        </html>
    );
}
