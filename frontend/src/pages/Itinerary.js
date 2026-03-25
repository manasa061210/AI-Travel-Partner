import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { userApi } from '../services/api';
import './Itinerary.css';

const SLOT_ICONS = { morning: '🌅', afternoon: '☀️', evening: '🌆' };

function Itinerary() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [trip, setTrip] = useState(null);
  const [itinerary, setItinerary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    userApi.getTrip(id).then(res => {
      const t = res.data.data;
      setTrip(t);
      // plan may be nested
      const plan = typeof t.plan === 'string' ? JSON.parse(t.plan) : t.plan;
      setItinerary(plan);
    }).catch(() => navigate('/dashboard'))
      .finally(() => setLoading(false));
  }, [id, navigate]);

  if (loading) return <div className="itin-loading"><div className="gen-spinner large" />Loading itinerary...</div>;
  if (!trip) return null;

  const plan = itinerary || {};
  const budget = plan.budget_estimate || {};
  const breakdown = budget.breakdown || {};
  const days = plan.days || plan.days_plan || [];
  const total = budget.total || trip.total_cost || 0;

  return (
    <div className="itinerary-page">
      {/* Header */}
      <div className="itin-hero">
        <div className="container">
          <div className="itin-hero-content">
            <div>
              <div className="itin-breadcrumb" onClick={() => navigate('/dashboard')}>← Back to Dashboard</div>
              <h1>📍 {trip.destination}</h1>
              <div className="itin-meta">
                {trip.start_date && <span>📅 {trip.start_date}</span>}
                <span>🌙 {trip.days} days</span>
                <span>👥 {trip.travelers} traveller{trip.travelers > 1 ? 's' : ''}</span>
                <span className="itin-category">{plan.category || trip.hotel_category}</span>
              </div>
            </div>
            <div className="itin-budget-badge">
              <div className="budget-label">Total Budget</div>
              <div className="budget-amount">₹{total.toLocaleString()}</div>
              <div className="budget-per">₹{Math.round(total / trip.travelers).toLocaleString()}/person</div>
            </div>
          </div>
        </div>
      </div>

      <div className="container itin-body">
        <div className="itin-main">
          {/* Budget Breakdown */}
          {Object.keys(breakdown).length > 0 && (
            <div className="itin-card budget-card">
              <h2>💰 Budget Breakdown</h2>
              <div className="budget-breakdown-bars">
                {Object.entries(breakdown).map(([key, val]) => {
                  const pct = Math.round((val / total) * 100);
                  const colors = { accommodation: '#3949ab', transport: '#00acc1', food: '#43a047', activities: '#ff6f00', misc: '#9e9e9e' };
                  return (
                    <div key={key} className="breakdown-item">
                      <div className="breakdown-label">
                        <span>{key.charAt(0).toUpperCase() + key.slice(1)}</span>
                        <span>₹{val?.toLocaleString()} ({pct}%)</span>
                      </div>
                      <div className="breakdown-bar-track">
                        <div style={{ width: `${pct}%`, background: colors[key], height: '100%', borderRadius: 50, transition: 'width 1s ease' }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Day-by-Day Plan */}
          <div className="itin-card">
            <h2>📅 Day-by-Day Itinerary</h2>
            {days.length === 0 ? (
              <p className="empty-note">No itinerary data available. Try regenerating the plan.</p>
            ) : (
              <div className="days-timeline">
                {days.map(day => (
                  <div className="day-block" key={day.day}>
                    <div className="day-header">
                      <div className="day-num">Day {day.day}</div>
                      {day.date && <div className="day-date">{day.date}</div>}
                      <div className="day-cost">₹{(day.daily_cost || day.day_cost)?.toLocaleString()}</div>
                    </div>

                    <div className="day-activities">
                      {(day.activities || []).map((act, i) => (
                        <div className="activity-item" key={i}>
                          <div className="act-time">
                            <span>{act.emoji || SLOT_ICONS[act.time_slot] || '📍'}</span>
                            <span>{act.time}</span>
                          </div>
                          <div className="act-content">
                            <h4>{act.name || act.place}</h4>
                            <p>{act.description || act.activity}</p>
                            <div className="act-meta">
                              <span>⏱ {act.duration || act.duration_hrs}</span>
                              <span>₹{(act.cost || act.estimated_cost)?.toLocaleString()}</span>
                              <span className="act-type">{act.type}</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    {day.meals && (
                      <div className="day-meals">
                        <div className="meal"><span>🌅</span> <strong>Breakfast:</strong> {day.meals.breakfast}</div>
                        <div className="meal"><span>☀️</span> <strong>Lunch:</strong> {day.meals.lunch}</div>
                        <div className="meal"><span>🌙</span> <strong>Dinner:</strong> {day.meals.dinner}</div>
                      </div>
                    )}

                    {day.accommodation && (
                      <div className="day-stay">🏨 <strong>Stay:</strong> {day.accommodation}</div>
                    )}

                    {day.notes && <div className="day-note">💡 {day.notes}</div>}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Tips */}
          {plan.tips && plan.tips.length > 0 && (
            <div className="itin-card tips-card">
              <h2>💡 Travel Tips</h2>
              <ul className="tips-list">
                {plan.tips.map((tip, i) => <li key={i}>{tip}</li>)}
              </ul>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <aside className="itin-sidebar">
          {plan.highlights && plan.highlights.length > 0 && (
            <div className="itin-card">
              <h3>⭐ Highlights</h3>
              <ul className="highlights-list">
                {plan.highlights.map((h, i) => h && <li key={i}>📍 {h}</li>)}
              </ul>
            </div>
          )}

          <div className="itin-card trip-info-card">
            <h3>📋 Trip Info</h3>
            <div className="info-row"><span>Destination</span><strong>{trip.destination}</strong></div>
            <div className="info-row"><span>Duration</span><strong>{trip.days} days</strong></div>
            <div className="info-row"><span>Travelers</span><strong>{trip.travelers}</strong></div>
            <div className="info-row"><span>Hotel</span><strong style={{ textTransform: 'capitalize' }}>{trip.hotel_category}</strong></div>
            <div className="info-row"><span>Transport</span><strong style={{ textTransform: 'capitalize' }}>{trip.transport_type}</strong></div>
            <div className="info-row"><span>Status</span>
              <strong style={{ textTransform: 'capitalize', color: 'var(--success)' }}>{trip.status}</strong>
            </div>
          </div>

          <div className="itin-actions">
            <button onClick={() => navigate('/plan-trip')} className="btn-replan">Plan Another Trip</button>
            <button onClick={() => window.print()} className="btn-print">🖨️ Print</button>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default Itinerary;
