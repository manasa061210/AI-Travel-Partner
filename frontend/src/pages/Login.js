import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Login.css';

function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || '/dashboard';

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(form.email, form.password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (role) => {
    if (role === 'user') setForm({ email: 'user@travel.com', password: 'user123' });
    else setForm({ email: 'admin@travel.com', password: 'admin123' });
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <div className="auth-left-content">
          <div className="auth-logo">✈ TravelPartner</div>
          <h2>Plan smarter.<br />Travel better.</h2>
          <p>Your AI-powered companion for every journey — from dream to destination.</p>
          <div className="auth-features">
            <div className="auth-feat"><span>🤖</span> AI Itinerary Generation</div>
            <div className="auth-feat"><span>💰</span> Smart Budget Planning</div>
            <div className="auth-feat"><span>🗺️</span> Route Optimization</div>
          </div>
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <div className="auth-header">
            <h1>Welcome back!</h1>
            <p>Sign in to continue planning your adventures</p>
          </div>

          {error && <div className="auth-error">⚠️ {error}</div>}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" name="email" value={form.email} onChange={handleChange}
                placeholder="you@example.com" required />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" name="password" value={form.password} onChange={handleChange}
                placeholder="••••••••" required />
            </div>

            <button type="submit" className="auth-btn" disabled={loading}>
              {loading ? <><span className="spinner" /> Signing in...</> : 'Sign In →'}
            </button>
          </form>

          <div className="auth-demo">
            <p>Try demo accounts:</p>
            <div className="demo-btns">
              <button onClick={() => fillDemo('user')}>👤 Demo User</button>
              <button onClick={() => fillDemo('admin')}>⚙️ Demo Admin</button>
            </div>
          </div>

          <p className="auth-switch">
            Don't have an account? <Link to="/register">Create one →</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
