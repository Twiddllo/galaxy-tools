import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { EyeIcon, EyeOffIcon } from '@heroicons/react/outline';
import GTLogo from '../assets/GT-logo.png';
import { login as loginApi } from '../services/api';
import { useNavigate } from 'react-router-dom';

const fadeIn = {
  hidden: { opacity: 0, y: 40 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8 } },
};

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await loginApi(email, password);
      localStorage.setItem('access_token', res.access_token);
      localStorage.setItem('refresh_token', res.refresh_token);
      setLoading(false);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="w-full h-full bg-gradient-to-br from-galaxy-800/60 to-galaxy-900/90 animate-pulse" />
      </div>
      <motion.form
        className="z-10 flex flex-col items-center bg-galaxy-800/80 rounded-xl shadow-2xl px-8 py-10 w-full max-w-md backdrop-blur-md border border-galaxy-700"
        initial="hidden"
        animate="show"
        variants={fadeIn}
        onSubmit={handleLogin}
      >
        <img src={GTLogo} alt="GT Logo" className="w-16 h-16 mb-4" />
        <h2 className="text-3xl font-galaxy font-bold text-accent mb-2 tracking-widest">Sign In</h2>
        <p className="text-galaxy-300 mb-6 text-center">Welcome back to Galaxy Tools</p>
        <div className="w-full mb-4">
          <label className="block text-galaxy-200 mb-1">Email</label>
          <input
            type="email"
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div className="w-full mb-4 relative">
          <label className="block text-galaxy-200 mb-1">Password</label>
          <input
            type={showPassword ? 'text' : 'password'}
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent pr-10"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          <button
            type="button"
            className="absolute right-3 top-8 text-galaxy-400 hover:text-accent"
            onClick={() => setShowPassword(v => !v)}
            tabIndex={-1}
          >
            {showPassword ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
          </button>
        </div>
        {error && <div className="w-full text-red-400 text-sm mb-2 text-center animate-pulse">{error}</div>}
        <button
          type="submit"
          className="w-full py-2 rounded bg-accent text-galaxy-900 font-bold shadow-lg hover:scale-105 transition-transform mt-2 disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
        <div className="flex justify-between w-full mt-4 text-sm">
          <a href="/register" className="text-galaxy-300 hover:text-accent transition-colors">Create account</a>
          <a href="/forgot-password" className="text-galaxy-300 hover:text-accent transition-colors">Forgot password?</a>
        </div>
      </motion.form>
    </div>
  );
};

export default Login; 