import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const GitHubCallback = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      const urlParams = new URLSearchParams(location.search);
      const code = urlParams.get('code');

      if (code) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/api/auth/oauth/github', { code });
          console.log('GitHub auth successful:', response.data);

          // Save token and user info to local storage
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify(response.data.user));

          // Redirect to dashboard
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
};

export default GitHubCallback;

