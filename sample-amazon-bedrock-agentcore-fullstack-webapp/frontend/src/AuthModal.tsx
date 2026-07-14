import { useState } from 'react';
import Modal from '@cloudscape-design/components/modal';
import Box from '@cloudscape-design/components/box';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Button from '@cloudscape-design/components/button';
import FormField from '@cloudscape-design/components/form-field';
import Input from '@cloudscape-design/components/input';
import Alert from '@cloudscape-design/components/alert';
import { signUp, signIn, confirmSignUp, completeNewPassword } from './auth';
import type { CognitoUser } from 'amazon-cognito-identity-js';

interface AuthModalProps {
  visible: boolean;
  onDismiss: () => void;
  onSuccess: () => void;
}

type AuthMode = 'signin' | 'signup' | 'confirm' | 'new-password';

export default function AuthModal({ visible, onDismiss, onSuccess }: AuthModalProps) {
  const [mode, setMode] = useState<AuthMode>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [confirmCode, setConfirmCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [pendingCognitoUser, setPendingCognitoUser] = useState<CognitoUser | null>(null);

  const handleSignIn = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await signIn(email, password);
      if (result.type === 'newPasswordRequired') {
        setPendingCognitoUser(result.cognitoUser);
        setMode('new-password');
      } else {
        onSuccess();
        resetForm();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to sign in');
    } finally {
      setLoading(false);
    }
  };

  const handleNewPassword = async () => {
    if (newPassword !== confirmNewPassword) {
      setError('Passwords do not match');
      return;
    }
    if (!pendingCognitoUser) return;
    setLoading(true);
    setError('');
    try {
      await completeNewPassword(pendingCognitoUser, newPassword);
      onSuccess();
      resetForm();
    } catch (err: any) {
      setError(err.message || 'Failed to set new password');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUp = async () => {
    setLoading(true);
    setError('');
    try {
      await signUp(email, password);
      setMode('confirm');
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to sign up');
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    setLoading(true);
    setError('');
    try {
      await confirmSignUp(email, confirmCode);
      const result = await signIn(email, password);
      if (result.type === 'newPasswordRequired') {
        setPendingCognitoUser(result.cognitoUser);
        setMode('new-password');
      } else {
        onSuccess();
        resetForm();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to confirm account');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setEmail('');
    setPassword('');
    setNewPassword('');
    setConfirmNewPassword('');
    setConfirmCode('');
    setMode('signin');
    setError('');
    setPendingCognitoUser(null);
  };

  const handleDismiss = () => {
    resetForm();
    onDismiss();
  };

  return (
    <Modal
      visible={visible}
      onDismiss={handleDismiss}
      header={mode === 'signin' ? 'Sign In' : mode === 'signup' ? 'Sign Up' : mode === 'confirm' ? 'Confirm Account' : 'Set New Password'}
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button variant="link" onClick={handleDismiss}>
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={mode === 'signin' ? handleSignIn : mode === 'signup' ? handleSignUp : mode === 'confirm' ? handleConfirm : handleNewPassword}
              loading={loading}
            >
              {mode === 'signin' ? 'Sign In' : mode === 'signup' ? 'Sign Up' : mode === 'confirm' ? 'Confirm' : 'Set Password'}
            </Button>
          </SpaceBetween>
        </Box>
      }
    >
      <SpaceBetween size="m">
        {error && (
          <Alert type="error" dismissible onDismiss={() => setError('')}>
            {error}
          </Alert>
        )}

        {mode === 'new-password' ? (
          <>
            <Alert type="info">
              Your account requires a new password before you can sign in.
            </Alert>
            <FormField label="New Password">
              <Input
                value={newPassword}
                onChange={({ detail }) => setNewPassword(detail.value)}
                type="password"
                placeholder="Enter new password"
              />
            </FormField>
            <FormField label="Confirm New Password">
              <Input
                value={confirmNewPassword}
                onChange={({ detail }) => setConfirmNewPassword(detail.value)}
                type="password"
                placeholder="Confirm new password"
              />
            </FormField>
          </>
        ) : mode === 'confirm' ? (
          <>
            <Alert type="info">
              A verification code has been sent to {email}. Please enter it below.
            </Alert>
            <FormField label="Verification Code">
              <Input
                value={confirmCode}
                onChange={({ detail }) => setConfirmCode(detail.value)}
                placeholder="Enter 6-digit code"
              />
            </FormField>
          </>
        ) : (
          <>
            <FormField label="Email">
              <Input
                value={email}
                onChange={({ detail }) => setEmail(detail.value)}
                type="email"
                placeholder="your@email.com"
              />
            </FormField>

            <FormField label="Password">
              <Input
                value={password}
                onChange={({ detail }) => setPassword(detail.value)}
                type="password"
                placeholder="Enter password"
              />
            </FormField>

            {mode === 'signin' ? (
              <Box textAlign="center">
                Don't have an account?{' '}
                <Button variant="inline-link" onClick={() => setMode('signup')}>
                  Sign up
                </Button>
              </Box>
            ) : (
              <Box textAlign="center">
                Already have an account?{' '}
                <Button variant="inline-link" onClick={() => setMode('signin')}>
                  Sign in
                </Button>
              </Box>
            )}
          </>
        )}
      </SpaceBetween>
    </Modal>
  );
}
