import React, { useState, useEffect } from 'react';
import { adminApi, destinationsApi } from '../services/api';
import './AdminDashboard.css';

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [destinations, setDestinations] = useState([]);
  const [tab, setTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [showAddDest, setShowAddDest] = useState(false);
  const [newDest, setNewDest] = useState({ name: '', city: '', country: 'India', category: 'beach', base_cost_per_day: 2500, description: '', best_season: '', rating: 4.0 });
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    Promise.all([
      adminApi.stats(),
      adminApi.users(),
      destinationsApi.list(),
    ]).then(([s, u, d]) => {
      setStats(s.data.data);
      setUsers(u.data.data);
      setDestinations(d.data.data);
    }).finally(() => setLoading(false));
  }, []);

  const handleAddDest = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await adminApi.createDestination(newDest);
      setMsg('Destination added!');
      setShowAddDest(false);
      const res = await destinationsApi.list();
      setDestinations(res.data.data);
      setNewDest({ name: '', city: '', country: 'India', category: 'beach', base_cost_per_day: 2500, description: '', best_season: '', rating: 4.0 });
    } catch (e) { setMsg('Failed to add destination'); }
    finally { setSaving(false); }
  };

  const handleDeleteDest = async (id) => {
    if (!window.confirm('Delete this destination?')) return;
    await adminApi.deleteDestination(id);
    setDestinations(destinations.filter(d => d.id !== id));
  };

  if (loading) return <div className="admin-loading">Loading admin panel...</div>;

  return (
    <div className="admin-page">
      <div className="admin-hero">
        <div className="container">
          <h1>⚙️ Admin Dashboard</h1>
          <p>Manage destinations, users and view platform statistics</p>
        </div>
      </div>

      <div className="container admin-body">
        {/* Stats */}
        <div className="admin-stats">
          <div className="admin-stat"><span className="astat-icon">👥</span><div><strong>{stats?.total_users}</strong><span>Users</span></div></div>
          <div className="admin-stat"><span className="astat-icon">✈️</span><div><strong>{stats?.total_trips}</strong><span>Trips Planned</span></div></div>
          <div className="admin-stat"><span className="astat-icon">🌍</span><div><strong>{stats?.total_destinations}</strong><span>Destinations</span></div></div>
          <div className="admin-stat"><span className="astat-icon">⭐</span><div><strong>4.8</strong><span>Avg Rating</span></div></div>
        </div>

        {/* Tabs */}
        <div className="admin-tabs">
          {['overview', 'destinations', 'users'].map(t => (
            <button key={t} className={`tab-btn ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {msg && <div className="admin-msg">{msg}</div>}

        {/* Overview Tab */}
        {tab === 'overview' && (
          <div className="admin-section">
            <h2>Popular Destinations</h2>
            {stats?.popular_destinations?.length === 0 ? (
              <p className="empty-note">No trip data yet.</p>
            ) : (
              <div className="pop-dest-list">
                {(stats?.popular_destinations || []).map((d, i) => (
                  <div key={i} className="pop-dest-item">
                    <span className="pop-rank">#{i + 1}</span>
                    <span className="pop-name">{d.name}</span>
                    <div className="pop-bar-track">
                      <div className="pop-bar" style={{ width: `${Math.min(d.count * 20, 100)}%` }} />
                    </div>
                    <span className="pop-count">{d.count} trips</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Destinations Tab */}
        {tab === 'destinations' && (
          <div className="admin-section">
            <div className="section-title-row">
              <h2>Destinations ({destinations.length})</h2>
              <button className="btn-add" onClick={() => setShowAddDest(!showAddDest)}>+ Add Destination</button>
            </div>

            {showAddDest && (
              <form onSubmit={handleAddDest} className="add-dest-form">
                <h3>Add New Destination</h3>
                <div className="add-form-grid">
                  <div className="form-group"><label>Name *</label><input required value={newDest.name} onChange={e => setNewDest({ ...newDest, name: e.target.value })} /></div>
                  <div className="form-group"><label>City</label><input value={newDest.city} onChange={e => setNewDest({ ...newDest, city: e.target.value })} /></div>
                  <div className="form-group"><label>Country</label><input value={newDest.country} onChange={e => setNewDest({ ...newDest, country: e.target.value })} /></div>
                  <div className="form-group"><label>Category</label>
                    <select value={newDest.category} onChange={e => setNewDest({ ...newDest, category: e.target.value })}>
                      {['beach','mountain','cultural','relaxation','adventure','city'].map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </div>
                  <div className="form-group"><label>Base Cost/Day (₹)</label><input type="number" value={newDest.base_cost_per_day} onChange={e => setNewDest({ ...newDest, base_cost_per_day: parseFloat(e.target.value) })} /></div>
                  <div className="form-group"><label>Rating</label><input type="number" min="1" max="5" step="0.1" value={newDest.rating} onChange={e => setNewDest({ ...newDest, rating: parseFloat(e.target.value) })} /></div>
                  <div className="form-group full"><label>Description</label><textarea value={newDest.description} onChange={e => setNewDest({ ...newDest, description: e.target.value })} rows="2" /></div>
                  <div className="form-group"><label>Best Season</label><input value={newDest.best_season} onChange={e => setNewDest({ ...newDest, best_season: e.target.value })} placeholder="e.g. October to March" /></div>
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-save" disabled={saving}>{saving ? 'Saving...' : 'Add Destination'}</button>
                  <button type="button" className="btn-cancel" onClick={() => setShowAddDest(false)}>Cancel</button>
                </div>
              </form>
            )}

            <div className="admin-table-wrap">
              <table className="admin-table">
                <thead>
                  <tr><th>#</th><th>Name</th><th>Category</th><th>City</th><th>Cost/Day</th><th>Rating</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  {destinations.map((d, i) => (
                    <tr key={d.id}>
                      <td>{i + 1}</td>
                      <td><strong>{d.name}</strong></td>
                      <td><span className="cat-pill">{d.category}</span></td>
                      <td>{d.city}</td>
                      <td>₹{d.base_cost_per_day?.toLocaleString()}</td>
                      <td>⭐ {d.rating}</td>
                      <td>
                        <button className="tbl-delete" onClick={() => handleDeleteDest(d.id)}>Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {tab === 'users' && (
          <div className="admin-section">
            <h2>Users ({users.length})</h2>
            <div className="admin-table-wrap">
              <table className="admin-table">
                <thead>
                  <tr><th>#</th><th>Name</th><th>Email</th><th>Role</th><th>Joined</th></tr>
                </thead>
                <tbody>
                  {users.map((u, i) => (
                    <tr key={u.id}>
                      <td>{i + 1}</td>
                      <td><strong>{u.name}</strong></td>
                      <td>{u.email}</td>
                      <td><span className={`role-pill ${u.role}`}>{u.role}</span></td>
                      <td>{u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
