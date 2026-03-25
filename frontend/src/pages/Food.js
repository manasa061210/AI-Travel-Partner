import React, { useState, useEffect } from 'react';
import { aiApi } from '../services/api';
import './Food.css';

const DESTINATIONS = ['GOA', 'LADAKH', 'DARJEELING', 'MANALI', 'OOTY', 'KERALA', 'JAIPUR', 'VARANASI'];

function Food() {
  const [selected, setSelected] = useState('GOA');
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchFoods(selected);
  }, [selected]);

  const fetchFoods = async (destination) => {
    setLoading(true);
    setError('');
    setFoods([]);
    try {
      const res = await aiApi.foodRecommendations(destination);
      if (res.data.success) {
        setFoods(res.data.data.foods || []);
      } else {
        setError('Could not load recommendations.');
      }
    } catch (e) {
      setError('Failed to connect. Is the backend running?');
    }
    setLoading(false);
  };

  return (
    <div className="food-page">
      <div className="food-header">
        <div className="food-title-block">
          <h1 className="food-title">FOOD<br />GUIDE</h1>
          <p className="food-subtitle">AI-powered local flavors</p>
        </div>
        <span className="food-icon">🍽️</span>
      </div>

      {/* Destination selector */}
      <div className="food-dest-row">
        {DESTINATIONS.map(d => (
          <button
            key={d}
            className={`food-dest-btn ${selected === d ? 'active' : ''}`}
            onClick={() => setSelected(d)}
          >
            {d}
          </button>
        ))}
      </div>

      {/* Loading */}
      {loading && (
        <div className="food-loading">
          <div className="food-spinner" />
          <p>AI is fetching local food picks for {selected}...</p>
        </div>
      )}

      {/* Error */}
      {error && <div className="food-error">{error}</div>}

      {/* Food cards */}
      {!loading && !error && (
        <div className="food-list">
          {foods.map((food, i) => (
            <div key={i} className="food-card">
              <div className="food-card-left">
                <span className="food-emoji">{food.emoji}</span>
              </div>
              <div className="food-card-body">
                <div className="food-card-top">
                  <span className="food-name">{food.name}</span>
                  {food.must_try && <span className="must-badge">Must Try</span>}
                </div>
                <span className="food-type">{food.type}</span>
                <p className="food-desc">{food.description}</p>
                <span className="food-price">{food.price_range}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Food;
