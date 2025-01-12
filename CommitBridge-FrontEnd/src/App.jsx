import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { ThemeProvider } from "@/components/theme-provider"
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import ProfilePage from './pages/ProfilePage'
import PasswordManagement from './pages/PasswordManagement'
import ProtectedRoute from './components/ProtectedRoute';
import GitHubCallback from './components/GitHubCallback';
import { AlertProvider } from '@/components/AlertProvider'

export default function App() {
  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <AlertProvider>
          <Router>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route element={<ProtectedRoute />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/change-password" element={<PasswordManagement />} />
                <Route path="/set-password" element={<PasswordManagement />} />
              </Route>
              <Route path="/forgot-password" element={<PasswordManagement />} />
              <Route path="/reset-password-confirm/:token" element={<PasswordManagement />} />
              <Route path="/github/callback" element={<GitHubCallback />} />
            </Routes>
          </Router>
        </AlertProvider>
      </ThemeProvider>
    </GoogleOAuthProvider>
  )
}

