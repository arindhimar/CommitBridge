import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Github } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useGoogleLogin } from '@react-oauth/google'
import axios from 'axios'
import { useNavigate } from 'react-router-dom';

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
        await sendUserDataToBackend({
          ...userInfo.data,
          provider: 'google',
        });
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
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&scope=user,repo`;
  };

  const sendUserDataToBackend = async (userData) => {
    try {
      const endpoint = isRegistering ? 'http://127.0.0.1:5000/api/auth/oauth/google' : 'http://127.0.0.1:5000/api/auth/oauth/google';
      const response = await axios.post(endpoint, userData);
      console.log('User action successful:', response.data);
      
      // Save token and user info to local storage
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      onClose();
      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err) {
      setError(isRegistering ? 'Failed to register' : 'Failed to log in');
      console.error(err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendUserDataToBackend({ email, password, username });
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
          <form onSubmit={handleSubmit}>
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
            </div>
            <Button type="submit" className="w-full mb-4">
              {isRegistering ? 'Register' : 'Login'}
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
              {/* Google icon SVG path */}
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

