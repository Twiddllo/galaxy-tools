import React, { useState } from 'react';
import { motion } from 'framer-motion';
import GTLogo from '../assets/GT-logo.png';
import { forgotPassword as forgotPasswordApi } from '../services/api';

const fadeIn = {
  hidden: { opacity: 0, y: 40 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8 } },
};

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await forgotPasswordApi(email);
      setSubmitted(true);
    } catch (err: any) {
      setError(err.message);
    }
    setLoading(false);
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
        onSubmit={handleSubmit}
      >
        <img src={GTLogo} alt="GT Logo" className="w-16 h-16 mb-4" />
        <h2 className="text-3xl font-galaxy font-bold text-accent mb-2 tracking-widest">Forgot Password</h2>
        <p className="text-galaxy-300 mb-6 text-center">Enter your email to receive a password reset link.</p>
        {!submitted ? (
          <>
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
            <button
              type="submit"
              className="w-full py-2 rounded bg-accent text-galaxy-900 font-bold shadow-lg hover:scale-105 transition-transform mt-2 disabled:opacity-60"
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Send Reset Link'}
            </button>
          </>
        ) : (
          <div className="w-full text-center text-galaxy-300 mt-4 animate-fade-in">
            If the email exists, a reset link has been sent.<br />
            <a href="/login" className="text-accent font-bold hover:underline mt-4 inline-block">Back to Login</a>
          </div>
        )}
      </motion.form>
    </div>
  );
};

export default ForgotPassword; 