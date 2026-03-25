import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { userApi, aiApi } from '../services/api';
import './Dashboard.css';

const STATUS_COLORS = { planned: '#3949ab', ongoing: '#f59e0b', completed: '#43a047' };

function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [trips, setTrips] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      userApi.getTrips(),
      aiApi.recommend({
        budget: 15000,
        interests: user?.preferences?.interests || ['beach', 'cultural'],
        duration: 3,
        travelers: 1,
      }).catch(() => null),
    ]).then(([tripsRes, recRes]) => {
      setTrips(tripsRes.data.data || []);
      if (recRes?.data?.data?.ranked) setRecommendations(recRes.data.data.ranked.slice(0, 3));
    }).finally(() => setLoading(false));
  }, [user]);

  const deleteTrip = async (id) => {
    if (!window.confirm('Delete this trip?')) return;
    await userApi.deleteTrip(id);
    setTrips(trips.filter(t => t.id !== id));
  };

  const upcoming = trips.filter(t => t.status === 'planned').length;
  const completed = trips.filter(t => t.status === 'completed').length;

  return (
    <div className="dashboard">
      <div className="dashboard-hero">
        <div className="container">
          <div className="dash-welcome">
            <div>
              <h1>Welcome back, {user?.name?.split(' ')[0]}! 🌍</h1>
              <p>Ready to plan your next adventure?</p>
            </div>
            <Link to="/plan-trip" className="btn-plan-new">✈ Plan New Trip</Link>
          </div>

          <div className="stats-cards">
            <div className="stat-card">
              <span className="stat-icon">🗺️</span>
              <div><strong>{trips.length}</strong><span>Total Trips</span></div>
            </div>
            <div className="stat-card">
              <span className="stat-icon">📅</span>
              <div><strong>{upcoming}</strong><span>Upcoming</span></div>
            </div>
            <div className="stat-card">
              <span className="stat-icon">✅</span>
              <div><strong>{completed}</strong><span>Completed</span></div>
            </div>
            <div className="stat-card">
              <span className="stat-icon">💰</span>
              <div>
                <strong>₹{trips.reduce((s, t) => s + (t.total_cost || 0), 0).toLocaleString()}</strong>
                <span>Total Planned</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container dashboard-body">
        <div className="dash-main">
          <section className="trips-section">
            <div className="section-title">
              <h2>My Trips</h2>
              <Link to="/plan-trip">+ New Trip</Link>
            </div>

            {loading ? (
              <div className="loading-state">Loading your trips...</div>
            ) : trips.length === 0 ? (
              <div className="empty-trips">
                <span>🗺️</span>
                <h3>No trips yet!</h3>
                <p>Start planning your first AI-powered adventure.</p>
                <Link to="/plan-trip" className="btn-primary">Plan Your First Trip</Link>
              </div>
            ) : (
              <div className="trips-grid">
                {trips.map(trip => (
                  <div className="trip-card" key={trip.id}>
                    <div className="trip-card-header">
                      <div>
                        <h3>{trip.title || `Trip to ${trip.destination}`}</h3>
                        <p className="trip-dest">📍 {trip.destination}</p>
                      </div>
                      <span className="trip-status" style={{ background: STATUS_COLORS[trip.status] }}>
                        {trip.status}
                      </span>
                    </div>
                    <div className="trip-meta">
                      <span>📆 {trip.start_date || 'Date TBD'}</span>
                      <span>🌙 {trip.days} days</span>
                      <span>👥 {trip.travelers} traveller{trip.travelers > 1 ? 's' : ''}</span>
                    </div>
                    <div className="trip-cost">
                      Total Budget: <strong>₹{(trip.total_cost || trip.budget || 0).toLocaleString()}</strong>
                    </div>
                    <div className="trip-actions">
                      <button onClick={() => navigate(`/itinerary/${trip.id}`)} className="btn-view">View Itinerary</button>
                      <button onClick={() => deleteTrip(trip.id)} className="btn-delete">🗑️</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        <aside className="dash-sidebar">
          <section className="rec-section">
            <h2>🤖 AI Picks for You</h2>
            <p className="rec-subtitle">Based on your interests</p>
            {recommendations.length === 0 ? (
              <div className="loading-state">Loading recommendations...</div>
            ) : (
              <div className="rec-list">
                {recommendations.map((dest, i) => (
                  <div className="rec-card" key={i}>
                    <div className="rec-rank">#{i + 1}</div>
                    <div className="rec-info">
                      <h4>{dest.name}</h4>
                      <p>{dest.category} • ₹{dest.base_cost_per_day?.toLocaleString()}/day</p>
                      <div className="rec-score">Match: {Math.round((dest.mcda_score || 0.7) * 100)}%</div>
                    </div>
                    <Link to={`/plan-trip?destination=${dest.name}`} className="rec-btn">Plan →</Link>
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="quick-links">
            <h2>Quick Actions</h2>
            <Link to="/destinations" className="quick-link">🌍 Browse Destinations</Link>
            <Link to="/plan-trip" className="quick-link">✈ Plan a Trip</Link>
            <Link to="/profile" className="quick-link">👤 Edit Profile</Link>
          </section>
        </aside>
      </div>
    </div>
  );
}

export default Dashboard;
