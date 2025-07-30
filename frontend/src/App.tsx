import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import GTLogo from './assets/GT-logo.png';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';

const fadeIn = {
  hidden: { opacity: 0, y: 40 },
  show: { opacity: 1, y: 0, transition: { duration: 1 } },
};

const Landing = () => (
  <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden">
    <div className="absolute inset-0 z-0 pointer-events-none">
      <div className="w-full h-full bg-gradient-to-br from-galaxy-800/60 to-galaxy-900/90 animate-pulse" />
    </div>
    <motion.div
      className="z-10 flex flex-col items-center"
      initial="hidden"
      animate="show"
      variants={fadeIn}
    >
      <img src={GTLogo} alt="Galaxy Tools Logo" className="w-32 h-32 mb-6 drop-shadow-lg" />
      <h1 className="text-5xl font-galaxy font-bold text-accent mb-2 tracking-widest">Galaxy Tools</h1>
      <p className="text-xl text-galaxy-300 mb-8 text-center max-w-xl">
        The #1 Twitch & Kick Automation Platform. Automate followers, views, chats, and more with cosmic power.
      </p>
      <div className="flex gap-4">
        <a href="/login" className="px-6 py-2 rounded bg-accent text-galaxy-900 font-bold shadow-lg hover:scale-105 transition-transform">Login</a>
        <a href="/register" className="px-6 py-2 rounded border-2 border-accent text-accent font-bold shadow-lg hover:bg-accent hover:text-galaxy-900 transition-colors">Register</a>
      </div>
    </motion.div>
    <footer className="absolute bottom-4 w-full text-center text-galaxy-300 text-xs z-10">
      &copy; {new Date().getFullYear()} Galaxy Tools. All rights reserved.
    </footer>
  </div>
);

function App() {
  return (
    <Router>
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Routes>
      </AnimatePresence>
    </Router>
  );
}

export default App;
