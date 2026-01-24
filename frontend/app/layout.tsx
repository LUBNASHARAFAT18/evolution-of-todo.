import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/lib/auth.context';

export const metadata: Metadata = {
  title: 'Evolution of Todo',
  description: 'Hackathon Phase II',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
