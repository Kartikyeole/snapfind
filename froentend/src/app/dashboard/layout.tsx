import type { Metadata } from "next";
import localFont from "next/font/local";
import "../globals.css";
import Sidebar from "@/components/sidebar/page";

const geistSans = localFont({
    src: "../fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});
const geistMono = localFont({
    src: "../fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

export const metadata: Metadata = {
    title: "Dashboard",
    description: "Dashboard page",
};

export default function DashboardLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased`}
            >
                <main className="flex">
                    <Sidebar />
                    <div className="">{children}</div>
                </main>
                
            </body>
        </html>
    );
}
