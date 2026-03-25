import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { destinationsApi } from '../services/api';
import './Destinations.css';

const CATEGORY_COLORS = {
  beach:      'linear-gradient(135deg, #0093E9, #80D0C7)',
  mountain:   'linear-gradient(135deg, #4776E6, #8E54E9)',
  cultural:   'linear-gradient(135deg, #f7971e, #ffd200)',
  relaxation: 'linear-gradient(135deg, #43e97b, #38f9d7)',
  adventure:  'linear-gradient(135deg, #f953c6, #b91d73)',
  city:       'linear-gradient(135deg, #4facfe, #00f2fe)',
};
const CATEGORY_EMOJI = { beach:'🏖️', mountain:'🏔️', cultural:'🏛️', relaxation:'🌿', adventure:'🧗', city:'🏙️' };
const CATEGORIES = ['all', 'beach', 'mountain', 'cultural', 'relaxation', 'adventure', 'city'];

function StarRating({ rating }) {
  return (
    <span className="stars">
      {[1,2,3,4,5].map(i => (
        <span key={i} style={{ color: i <= Math.round(rating) ? '#f59e0b' : '#d1d5db' }}>★</span>
      ))}
      <span className="rating-val">{rating}</span>
    </span>
  );
}

function Destinations() {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [budgetMax, setBudgetMax] = useState('');
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    destinationsApi.list().then(res => setDestinations(res.data.data || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = destinations.filter(d => {
    if (search && !d.name.toLowerCase().includes(search.toLowerCase()) &&
        !d.description?.toLowerCase().includes(search.toLowerCase())) return false;
    if (category !== 'all' && d.category !== category) return false;
    if (budgetMax && d.base_cost_per_day > parseInt(budgetMax)) return false;
    return true;
  });

  return (
    <div className="destinations-page">
      <div className="dest-hero">
        <div className="container">
          <h1>Explore Destinations 🌍</h1>
          <p>Discover amazing places across India, filtered to match your travel style</p>
        </div>
      </div>

      <div className="container dest-body">
        {/* Filters */}
        <aside className="dest-filters">
          <h3>Filter</h3>

          <div className="filter-group">
            <label>Search</label>
            <input type="text" placeholder="Search destinations..."
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>

          <div className="filter-group">
            <label>Category</label>
            <div className="cat-btns">
              {CATEGORIES.map(c => (
                <button key={c} className={`cat-btn ${category === c ? 'active' : ''}`}
                  onClick={() => setCategory(c)}>
                  {c === 'all' ? '🌐 All' : `${CATEGORY_EMOJI[c]} ${c.charAt(0).toUpperCase() + c.slice(1)}`}
                </button>
              ))}
            </div>
          </div>

          <div className="filter-group">
            <label>Max Budget (₹/day)</label>
            <input type="number" placeholder="e.g. 3000" value={budgetMax}
              onChange={e => setBudgetMax(e.target.value)} min="0" />
          </div>

          <button className="btn-clear" onClick={() => { setSearch(''); setCategory('all'); setBudgetMax(''); }}>
            Clear Filters
          </button>
        </aside>

        {/* Grid */}
        <div className="dest-content">
          <div className="dest-count">
            {loading ? 'Loading...' : `${filtered.length} destination${filtered.length !== 1 ? 's' : ''} found`}
          </div>

          {loading ? (
            <div className="loading-grid">
              {[1,2,3,4,5,6].map(i => <div key={i} className="card-skeleton" />)}
            </div>
          ) : filtered.length === 0 ? (
            <div className="no-results">
              <span>🔍</span>
              <h3>No destinations found</h3>
              <p>Try adjusting your filters</p>
            </div>
          ) : (
            <div className="dest-grid">
              {filtered.map(dest => (
                <div className="dest-card" key={dest.id} onClick={() => setSelected(dest)}>
                  <div className="dest-img" style={{ background: CATEGORY_COLORS[dest.category] || CATEGORY_COLORS.city }}>
                    <span className="dest-emoji-lg">{CATEGORY_EMOJI[dest.category] || '📍'}</span>
                    <span className="cat-badge">{dest.category}</span>
                  </div>
                  <div className="dest-body-card">
                    <div className="dest-top">
                      <div>
                        <h3>{dest.name}</h3>
                        <p>📍 {dest.city}, {dest.country}</p>
                      </div>
                      <div className="dest-price">
                        <span>From</span>
                        <strong>₹{dest.base_cost_per_day?.toLocaleString()}<small>/day</small></strong>
                      </div>
                    </div>
                    <StarRating rating={dest.rating} />
                    <p className="dest-desc">{dest.description}</p>
                    <div className="dest-footer">
                      <span className="season-badge">📅 {dest.best_season}</span>
                      <button className="btn-details">Details →</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {selected && (
        <div className="dest-modal-overlay" onClick={() => setSelected(null)}>
          <div className="dest-modal" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelected(null)}>✕</button>

            <div className="modal-img" style={{ background: CATEGORY_COLORS[selected.category] || CATEGORY_COLORS.city }}>
              <span>{CATEGORY_EMOJI[selected.category] || '📍'}</span>
              <span className="cat-badge">{selected.category}</span>
            </div>

            <div className="modal-body">
              <div className="modal-header">
                <div>
                  <h2>{selected.name}</h2>
                  <p>📍 {selected.city}, {selected.country}</p>
                  <StarRating rating={selected.rating} />
                </div>
                <div className="modal-price">
                  <span>From</span>
                  <strong>₹{selected.base_cost_per_day?.toLocaleString()}<small>/day</small></strong>
                </div>
              </div>

              <p className="modal-desc">{selected.description}</p>

              <div className="modal-info">
                <div className="info-item"><strong>🌤 Best Season</strong><span>{selected.best_season}</span></div>
                <div className="info-item"><strong>🌡 Weather</strong><span>{selected.weather_info}</span></div>
              </div>

              {selected.popular_attractions?.length > 0 && (
                <div className="modal-attractions">
                  <h4>Popular Attractions</h4>
                  <div className="attractions-grid">
                    {selected.popular_attractions.map((a, i) => (
                      <div className="attraction-chip" key={i}>
                        <span>📍</span>
                        <div>
                          <p>{a.name}</p>
                          <span>⭐ {a.rating} · {a.duration_hrs}h</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <Link to={`/plan-trip?destination=${selected.name}`} className="btn-plan-here">
                ✈ Plan Trip to {selected.name}
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Destinations;
