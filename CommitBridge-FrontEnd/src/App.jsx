import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { ThemeProvider } from "@/components/theme-provider"
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import ProfilePage from './pages/ProfilePage'
import ProtectedRoute from './components/ProtectedRoute';
import GitHubCallback from './components/GitHubCallback';

export default function App() {
  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Router>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
            <Route path="/github/callback" element={<GitHubCallback />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </GoogleOAuthProvider>
  )
}

