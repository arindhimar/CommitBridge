import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function GitHubCallback() {
  const [error, setError] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const searchParams = new URLSearchParams(location.search);
      const code = searchParams.get('code');

      if (code) {
        try {
          // Exchange the code for an access token
          const tokenResponse = await axios.post('/api/auth/github', { code });
          const { access_token } = tokenResponse.data;

          // Fetch user data
          const userResponse = await axios.get('https://api.github.com/user', {
            headers: { Authorization: `Bearer ${access_token}` },
          });

          console.log('GitHub User Info:', userResponse.data);

          // Send user data to your backend
          await axios.post('/api/auth/register', {
            ...userResponse.data,
            provider: 'github',
          });

          // Redirect to the dashboard or home page
          navigate('/dashboard');
        } catch (err) {
          setError('Failed to authenticate with GitHub');
          console.error(err);
        }
      } else {
        setError('No code provided by GitHub');
      }
    };

    fetchData();
  }, [location, navigate]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return <div>Authenticating with GitHub...</div>;
}

