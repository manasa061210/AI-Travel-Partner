import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { userApi } from '../services/api';
import './Profile.css';

const INTERESTS = ['Adventure', 'Relaxation', 'Cultural', 'Beach', 'Mountain', 'City', 'Food', 'Shopping', 'Wildlife', 'Spiritual'];

function Profile() {
  const { user, updateUser } = useAuth();
  const [form, setForm] = useState({ name: user?.name || '', email: user?.email || '', password: '', confirm: '' });
  const [interests, setInterests] = useState(user?.preferences?.interests?.map(i => i.charAt(0).toUpperCase() + i.slice(1)) || []);
  const [budgetPref, setBudgetPref] = useState(user?.preferences?.budget_pref || 'standard');
  const [trips, setTrips] = useState([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    userApi.getTrips().then(res => setTrips(res.data.data || [])).catch(() => {});
  }, []);

  const toggleInterest = (i) => {
    setInterests(prev => prev.includes(i) ? prev.filter(x => x !== i) : [...prev, i]);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setMessage(''); setError('');
    if (form.password && form.password !== form.confirm) return setError('Passwords do not match');
    setSaving(true);
    try {
      const payload = {
        name: form.name,
        preferences: { interests: interests.map(i => i.toLowerCase()), budget_pref: budgetPref },
      };
      if (form.password) payload.password = form.password;
      const res = await userApi.updateProfile(payload);
      updateUser(res.data.data);
      setMessage('Profile updated successfully!');
      setForm(prev => ({ ...prev, password: '', confirm: '' }));
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const initials = user?.name?.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);

  return (
    <div className="profile-page">
      <div className="profile-hero">
        <div className="container">
          <div className="profile-header">
            <div className="profile-avatar">{initials}</div>
            <div>
              <h1>{user?.name}</h1>
              <p>{user?.email}</p>
              <span className="role-badge">{user?.role === 'admin' ? '⚙️ Admin' : '👤 Traveller'}</span>
            </div>
          </div>
          <div className="profile-stats">
            <div className="pstat"><strong>{trips.length}</strong><span>Trips</span></div>
            <div className="pstat"><strong>{trips.reduce((s, t) => s + (t.days || 0), 0)}</strong><span>Days Planned</span></div>
            <div className="pstat"><strong>₹{trips.reduce((s, t) => s + (t.total_cost || 0), 0).toLocaleString()}</strong><span>Total Budgeted</span></div>
          </div>
        </div>
      </div>

      <div className="container profile-body">
        <form onSubmit={handleSave} className="profile-card">
          <h2>Edit Profile</h2>

          {message && <div className="profile-success">✅ {message}</div>}
          {error && <div className="auth-error">⚠️ {error}</div>}

          <div className="profile-form">
            <div className="form-group">
              <label>Full Name</label>
              <input type="text" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" value={form.email} disabled style={{ opacity: 0.6, cursor: 'not-allowed' }} />
            </div>
            <div className="form-group">
              <label>New Password <small>(leave blank to keep current)</small></label>
              <input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} placeholder="New password" />
            </div>
            <div className="form-group">
              <label>Confirm Password</label>
              <input type="password" value={form.confirm} onChange={e => setForm({ ...form, confirm: e.target.value })} placeholder="Confirm new password" />
            </div>

            <div className="form-group full">
              <label>Travel Interests</label>
              <div className="interests-grid">
                {INTERESTS.map(i => (
                  <button type="button" key={i}
                    className={`interest-tag ${interests.includes(i) ? 'selected' : ''}`}
                    onClick={() => toggleInterest(i)}>{i}</button>
                ))}
              </div>
            </div>

            <div className="form-group full">
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
          </div>

          <button type="submit" className="auth-btn" disabled={saving}>
            {saving ? <><span className="spinner" /> Saving...</> : 'Save Changes'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Profile;
