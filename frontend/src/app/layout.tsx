import type { Metadata } from "next";
import { Providers } from "@/components/providers";
import localFont from "next/font/local";
import "./globals.css";

const rocGrotesk = localFont({
  src: [
    {
      path: './fonts/roc_grotesk/Fontspring-DEMO-rocgrotesk-regular.otf',
      weight: '400',
      style: 'normal',
    },
    {
      path: './fonts/roc_grotesk/Fontspring-DEMO-rocgrotesk-medium.otf',
      weight: '500',
      style: 'normal',
    },
    {
      path: './fonts/roc_grotesk/Fontspring-DEMO-rocgrotesk-bold.otf',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-roc-grotesk',
  display: 'swap',
});

export const metadata: Metadata = {
  title: "Kryptt",
  description: "Building the future of AI, one line at a time.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${rocGrotesk.variable} font-roc antialiased`}>
        <Providers
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </Providers>
      </body>
    </html>
  );
}
