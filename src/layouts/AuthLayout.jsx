import { Outlet } from 'react-router-dom';
import { motion } from 'framer-motion';
import './AuthLayout.css';

const AuthLayout = () => {
  return (
    <div className="auth-layout">
      <div className="auth-background">
        <div className="auth-gradient auth-gradient-1"></div>
        <div className="auth-gradient auth-gradient-2"></div>
        <div className="auth-gradient auth-gradient-3"></div>
      </div>
      
      <motion.div 
        className="auth-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="auth-brand">
          <h1>
            <span className="brand-gradient">Vibe</span>
            <span>Graph</span>
          </h1>
          <p className="auth-tagline">
            Discover your aesthetic identity through AI-powered cultural connections
          </p>
        </div>
        
        <div className="auth-card">
          <Outlet />
        </div>
        
        <p className="auth-footer">
          By continuing, you agree to our Terms & Privacy Policy
        </p>
      </motion.div>
    </div>
  );
};

export default AuthLayout;
