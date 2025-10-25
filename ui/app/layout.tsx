import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinWise - Sistem Pakar Alokasi Aset Investasi",
  description: "Sistem pakar untuk menentukan alokasi aset investasi berdasarkan profil risiko dan tujuan finansial pengguna.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
      >
        {children}
      </body>
    </html>
  );
}
