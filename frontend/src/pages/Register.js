import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Login.css';
import './Register.css';

const INTERESTS = ['Adventure', 'Relaxation', 'Cultural', 'Beach', 'Mountain', 'City', 'Food', 'Shopping', 'Wildlife', 'Spiritual'];

function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '' });
  const [interests, setInterests] = useState([]);
  const [budgetPref, setBudgetPref] = useState('standard');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const toggleInterest = (i) => {
    setInterests(prev => prev.includes(i) ? prev.filter(x => x !== i) : [...prev, i]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (form.password !== form.confirm) return setError('Passwords do not match');
    if (form.password.length < 6) return setError('Password must be at least 6 characters');
    setLoading(true);
    try {
      await register({
        name: form.name,
        email: form.email,
        password: form.password,
        preferences: { interests: interests.map(i => i.toLowerCase()), budget_pref: budgetPref },
      });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <div className="auth-left-content">
          <div className="auth-logo">✈ TravelPartner</div>
          <h2>Start your journey today.</h2>
          <p>Join thousands of smart travellers who plan smarter trips with AI.</p>
          <div className="auth-features">
            <div className="auth-feat"><span>🆓</span> Free to use</div>
            <div className="auth-feat"><span>🤖</span> AI-powered plans</div>
            <div className="auth-feat"><span>💾</span> Save unlimited trips</div>
          </div>
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-card register-card">
          <div className="auth-header">
            <h1>Create Account</h1>
            <p>Set up your traveller profile to get started</p>
          </div>

          {error && <div className="auth-error">⚠️ {error}</div>}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-row">
              <div className="form-group">
                <label>Full Name</label>
                <input type="text" name="name" value={form.name} onChange={handleChange} placeholder="Rahul Sharma" required />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Password</label>
                <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Min 6 characters" required />
              </div>
              <div className="form-group">
                <label>Confirm Password</label>
                <input type="password" name="confirm" value={form.confirm} onChange={handleChange} placeholder="Repeat password" required />
              </div>
            </div>

            <div className="form-group">
              <label>Travel Interests (select all that apply)</label>
              <div className="interests-grid">
                {INTERESTS.map(i => (
                  <button type="button" key={i}
                    className={`interest-tag ${interests.includes(i) ? 'selected' : ''}`}
                    onClick={() => toggleInterest(i)}>
                    {i}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Budget Preference</label>
              <div className="budget-options">
                {['budget', 'standard', 'luxury'].map(b => (
                  <button type="button" key={b}
                    className={`budget-opt ${budgetPref === b ? 'selected' : ''}`}
                    onClick={() => setBudgetPref(b)}>
                    {b === 'budget' ? '💸 Budget' : b === 'standard' ? '🏨 Standard' : '👑 Luxury'}
                  </button>
                ))}
              </div>
            </div>

            <button type="submit" className="auth-btn" disabled={loading}>
              {loading ? <><span className="spinner" /> Creating account...</> : 'Create Account →'}
            </button>
          </form>

          <p className="auth-switch">Already have an account? <Link to="/login">Sign in →</Link></p>
        </div>
      </div>
    </div>
  );
}

export default Register;
