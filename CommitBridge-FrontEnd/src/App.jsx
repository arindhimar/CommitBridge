import React from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import OAuthSignUp from './components/OAuthSignUp';
import { ThemeProvider } from "./components/theme-provider";

function App() {
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  if (!googleClientId) {
    console.error('Google Client ID is not set. Please check your environment variables.');
    return <div>Error: Google Client ID is not configured.</div>;
  }

  return (
    <ThemeProvider defaultTheme="system" enableSystem>
      <GoogleOAuthProvider clientId={googleClientId}>
        <div className="App min-h-screen bg-background text-foreground">
          <header className="py-6">
            <h1 className="text-4xl font-bold text-center">CommitBridge</h1>
          </header>
          <main className="container mx-auto px-4">
            <OAuthSignUp />
          </main>
        </div>
      </GoogleOAuthProvider>
    </ThemeProvider>
  );
}

export default App;

