import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "./providers/AuthProvider";
import { spaceGrotesk } from "./fonts";

export const metadata: Metadata = {
  title: "Kryptt",
  description: "Trade stocks with simple commands",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${spaceGrotesk.variable} font-sans`}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
