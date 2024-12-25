import React, { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { Button } from "./ui/button";

export default function OAuthSignUp() {
  const [error, setError] = useState(null);

  const handleGoogleSignUp = useGoogleLogin({
    onSuccess: async (response) => {
      try {
        const userInfo = await axios.get(
          'https://www.googleapis.com/oauth2/v3/userinfo',
          {
            headers: { Authorization: `Bearer ${response.access_token}` },
          }
        );
        await sendUserDataToBackend({
          ...userInfo.data,
          github_access_token: null,
          github_username: null,
          provider: 'google',
        });
      } catch (err) {
        setError('Failed to get user info from Google');
        console.error(err);
      }
    },
    onError: (error) => {
      setError('Google sign-up failed');
      console.error(error);
    },
  });

  const handleGitHubSignUp = () => {
    const githubClientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
    if (!githubClientId) {
      setError('GitHub Client ID is not configured');
      return;
    }
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&scope=user,repo`;
  };

  const sendUserDataToBackend = async (userData) => {
    try {
      const response = await axios.post('/api/signup', userData);
      console.log('User created:', response.data);
      // Handle successful sign-up (e.g., redirect to dashboard)
    } catch (err) {
      setError('Failed to create user account');
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      <Button onClick={() => handleGoogleSignUp()} className="w-full max-w-md">
        Sign up with Google
      </Button>
      <Button onClick={handleGitHubSignUp} className="w-full max-w-md">
        Sign up with GitHub
      </Button>
      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
}

