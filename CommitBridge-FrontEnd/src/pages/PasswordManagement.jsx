import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAlert } from '@/components/AlertProvider';
import axios from 'axios';

const PasswordManagement = () => {
  const [email, setEmail] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { showAlert } = useAlert();
  const navigate = useNavigate();
  const location = useLocation();

  const isResetPassword = location.pathname === '/forgot-password';
  const isSetPassword = location.pathname === '/set-password';
  const isResetPasswordConfirm = location.pathname.startsWith('/reset-password-confirm/');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if ((isResetPassword || isSetPassword) && newPassword !== confirmPassword) {
      showAlert('error', 'New passwords do not match');
      return;
    }

    try {
      let endpoint, payload;
      if (isResetPassword) {
        endpoint = 'http://127.0.0.1:5000//api/auth/forgot-password';
        payload = { email };
      } else if (isSetPassword) {
        endpoint = 'http://127.0.0.1:5000//api/auth/set-password';
        payload = { 
          user_id: JSON.parse(localStorage.getItem('user')).id, 
          new_password: newPassword 
        };
      } else if (location.pathname.startsWith('/reset-password-confirm/')) {
        const token = location.pathname.split('/').pop();
        endpoint = `http://127.0.0.1:5000//api/auth/reset-password-confirm/${token}`;
        payload = { new_password: newPassword };
      } else {
        endpoint = 'http://127.0.0.1:5000//api/auth/change-password';
        payload = { 
          user_id: JSON.parse(localStorage.getItem('user')).id, 
          old_password: oldPassword, 
          new_password: newPassword 
        };
      }

      const response = await axios.post(endpoint, payload);
      showAlert('success', response.data.message);
      if (isResetPassword) {
        showAlert('info', 'Please check your email for further instructions');
      } else {
        navigate('/dashboard');
      }
    } catch (error) {
      showAlert('error', error.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex items-center justify-center min-h-screen bg-background"
    >
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>
            {isResetPassword ? 'Forgot Password' : isSetPassword ? 'Set Password' : 'Change Password'}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {(isResetPassword || isResetPasswordConfirm) && (
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required={isResetPassword}
                  disabled={isResetPasswordConfirm}
                />
              </div>
            )}
            {!isResetPassword && !isSetPassword && (
              <div>
                <Label htmlFor="oldPassword">Old Password</Label>
                <Input
                  id="oldPassword"
                  type="password"
                  value={oldPassword}
                  onChange={(e) => setOldPassword(e.target.value)}
                  required
                />
              </div>
            )}
            {!isResetPassword && (
              <>
                <div>
                  <Label htmlFor="newPassword">New Password</Label>
                  <Input
                    id="newPassword"
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="confirmPassword">Confirm New Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>
              </>
            )}
            <Button type="submit" className="w-full">
              {isResetPassword ? 'Send Reset Email' : 
               isResetPasswordConfirm ? 'Reset Password' :
               isSetPassword ? 'Set Password' : 'Change Password'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default PasswordManagement;

