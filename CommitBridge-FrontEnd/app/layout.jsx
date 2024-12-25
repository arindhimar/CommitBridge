import './globals.css';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/components/theme-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'CommitBridge - GitHub Activity Auto-Poster',
  description: 'Automate your daily work updates with AI',
  openGraph: {
    title: 'CommitBridge',
    description: 'Automate your daily work updates with AI',
    url: 'https://commitbridge.com',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'CommitBridge logo',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CommitBridge',
    description: 'Automate your daily work updates with AI',
    images: ['/twitter-image.png'],
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning aria-live="polite">
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
