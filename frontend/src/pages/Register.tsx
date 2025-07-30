import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { EyeIcon, EyeOffIcon } from '@heroicons/react/outline';
import GTLogo from '../assets/GT-logo.png';
import { register as registerApi } from '../services/api';
import { useNavigate } from 'react-router-dom';

const fadeIn = {
  hidden: { opacity: 0, y: 40 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8 } },
};

const Register: React.FC = () => {
  const [form, setForm] = useState({
    username: '',
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    setLoading(true);
    try {
      await registerApi(form);
      setSuccess('Registration successful! Check your email to verify your account.');
      setLoading(false);
      setTimeout(() => navigate('/login'), 2000);
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
        onSubmit={handleRegister}
      >
        <img src={GTLogo} alt="GT Logo" className="w-16 h-16 mb-4" />
        <h2 className="text-3xl font-galaxy font-bold text-accent mb-2 tracking-widest">Create Account</h2>
        <p className="text-galaxy-300 mb-6 text-center">Join the Galaxy Tools universe</p>
        <div className="w-full mb-3">
          <label className="block text-galaxy-200 mb-1">Username</label>
          <input
            name="username"
            type="text"
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent"
            value={form.username}
            onChange={handleChange}
            required
            autoFocus
          />
        </div>
        <div className="flex gap-2 w-full mb-3">
          <div className="flex-1">
            <label className="block text-galaxy-200 mb-1">First Name</label>
            <input
              name="firstName"
              type="text"
              className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent"
              value={form.firstName}
              onChange={handleChange}
              required
            />
          </div>
          <div className="flex-1">
            <label className="block text-galaxy-200 mb-1">Last Name</label>
            <input
              name="lastName"
              type="text"
              className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent"
              value={form.lastName}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="w-full mb-3">
          <label className="block text-galaxy-200 mb-1">Email</label>
          <input
            name="email"
            type="email"
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="w-full mb-3">
          <label className="block text-galaxy-200 mb-1">Phone <span className="text-galaxy-400 text-xs">(optional)</span></label>
          <input
            name="phone"
            type="tel"
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent"
            value={form.phone}
            onChange={handleChange}
          />
        </div>
        <div className="w-full mb-3 relative">
          <label className="block text-galaxy-200 mb-1">Password</label>
          <input
            name="password"
            type={showPassword ? 'text' : 'password'}
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent pr-10"
            value={form.password}
            onChange={handleChange}
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
        <div className="w-full mb-4 relative">
          <label className="block text-galaxy-200 mb-1">Confirm Password</label>
          <input
            name="confirmPassword"
            type={showConfirm ? 'text' : 'password'}
            className="w-full px-4 py-2 rounded bg-galaxy-900 border border-galaxy-700 text-white focus:outline-none focus:ring-2 focus:ring-accent pr-10"
            value={form.confirmPassword}
            onChange={handleChange}
            required
          />
          <button
            type="button"
            className="absolute right-3 top-8 text-galaxy-400 hover:text-accent"
            onClick={() => setShowConfirm(v => !v)}
            tabIndex={-1}
          >
            {showConfirm ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
          </button>
        </div>
        {error && <div className="w-full text-red-400 text-sm mb-2 text-center animate-pulse">{error}</div>}
        {success && <div className="w-full text-green-400 text-sm mb-2 text-center animate-pulse">{success}</div>}
        <button
          type="submit"
          className="w-full py-2 rounded bg-accent text-galaxy-900 font-bold shadow-lg hover:scale-105 transition-transform mt-2 disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Creating account...' : 'Create Account'}
        </button>
        <div className="flex justify-center w-full mt-4 text-sm">
          <a href="/login" className="text-galaxy-300 hover:text-accent transition-colors">Already have an account? Sign in</a>
        </div>
      </motion.form>
    </div>
  );
};

export default Register; 