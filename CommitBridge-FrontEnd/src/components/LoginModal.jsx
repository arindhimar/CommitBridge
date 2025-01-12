import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Github, Mail } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useGoogleLogin } from '@react-oauth/google'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'

export default function LoginModal({ isOpen, onClose }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [username, setUsername] = useState('')
  const [isRegistering, setIsRegistering] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate();

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (response) => {
      try {
        const userInfo = await axios.get(
          'https://www.googleapis.com/oauth2/v3/userinfo',
          {
            headers: { Authorization: `Bearer ${response.access_token}` },
          }
        );
        console.log('Google User Info:', userInfo.data);
        await sendUserDataToBackend(userInfo.data, 'google');
      } catch (err) {
        setError('Failed to get user info from Google');
        console.error(err);
      }
    },
    onError: (error) => {
      setError('Google login failed');
      console.error(error);
    },
  });

  const handleGitHubLogin = (e) => {
    e.preventDefault();
    const githubClientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
    if (!githubClientId) {
      setError('GitHub Client ID is not configured');
      return;
    }
    const redirectUri = encodeURIComponent(`${window.location.origin}/github/callback`);
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${redirectUri}&scope=user,repo`;
  };

  const sendUserDataToBackend = async (userData, method) => {
    let endpoint;
    switch (method) {
      case 'google':
        endpoint = 'http://127.0.0.1:5000/api/auth/oauth/google';
        break;
      case 'github':
        endpoint = 'http://127.0.0.1:5000/api/auth/oauth/github';
        break;
      case 'email':
        endpoint = isRegistering
          ? 'http://127.0.0.1:5000/api/auth/register'
          : 'http://127.0.0.1:5000/api/auth/login';
        break;
      default:
        setError('Invalid authentication method');
        return;
    }

    try {
      const response = await axios.post(endpoint, userData);
      console.log('User action successful:', response.data);
      
      // Save token and user info to local storage
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      onClose();
      
      // Check if password needs to be set (for Google login)
      if (response.data.requires_password_set) {
        navigate('/set-password');
      } else {
        // Redirect to dashboard
        navigate('/dashboard');
      }
    } catch (err) {
      setError(`Failed to authenticate using ${method}`);
      console.error(err);
    }
  };

  const handleEmailAuth = async (e) => {
    e.preventDefault();
    await sendUserDataToBackend({ email, password, username }, 'email');
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      >
        <motion.div
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md relative"
        >
          <button
            className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
            onClick={onClose}
          >
            <X size={20} />
          </button>
          <h2 className="text-2xl font-bold mb-4 text-center">
            {isRegistering ? 'Register' : 'Login'}
          </h2>
          <form onSubmit={handleEmailAuth}>
            <div className="mb-4">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            {isRegistering && (
              <div className="mb-4">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
            )}
            <div className="mb-4">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <Link to="/forgot-password" className="text-sm text-blue-600 hover:underline mt-1 block">
                Forgot password?
              </Link>
            </div>
            <Button type="submit" className="w-full mb-4">
              {isRegistering ? 'Register' : 'Login'} with Email
            </Button>
          </form>
          <div className="relative mb-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-gray-800 text-gray-500">Or continue with</span>
            </div>
          </div>
          <Button
            variant="outline"
            className="w-full flex items-center justify-center gap-2 mb-4"
            onClick={handleGitHubLogin}
          >
            <Github size={20} />
            Continue with GitHub
          </Button>
          <Button
            type="button"
            variant="outline"
            className="w-full flex items-center justify-center gap-2"
            onClick={() => handleGoogleLogin()}
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
              <path fill="none" d="M1 1h22v22H1z" />
            </svg>
            Continue with Google
          </Button>
          {error && <p className="mt-4 text-red-500 text-center">{error}</p>}
          <p className="mt-4 text-center text-sm">
            {isRegistering ? 'Already have an account?' : "Don't have an account?"}
            <button
              type="button"
              className="ml-1 text-blue-600 hover:underline"
              onClick={() => setIsRegistering(!isRegistering)}
            >
              {isRegistering ? 'Login' : 'Register'}
            </button>
          </p>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

