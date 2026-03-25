import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Home.css';

const DESTINATIONS = [
  {
    name: 'GOA',
    photo: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400&q=80',
  },
  {
    name: 'LADAKH',
    photo: 'https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=400&q=80',
  },
  {
    name: 'DARJEELING',
    photo: 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=400&q=80',
  },
  {
    name: 'MANALI',
    photo: 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&q=80',
  },
  {
    name: 'OOTY',
    photo: 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=400&q=80',
  },
  {
    name: 'KERALA',
    photo: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400&q=80',
  },
];

function Home() {
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const filtered = DESTINATIONS.filter(d =>
    d.name.includes(search.toUpperCase())
  );

  return (
    <div className="home">

      {/* Header */}
      <div className="home-header">
        <div className="home-title-block">
          <h1 className="home-title">AI-TRAVEL<br />PARTNER</h1>
          <p className="home-tagline">Adventure Awaits...</p>
        </div>
        <div className="home-bag">🎒</div>
      </div>

      {/* Search */}
      <div className="home-search-wrap">
        <div className="home-search">
          <span>🔍</span>
          <input
            type="text"
            placeholder="Search destinations..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && navigate(`/destinations?search=${search}`)}
          />
          {search && <button onClick={() => setSearch('')}>✕</button>}
        </div>
        <div className="home-search-icons">
          <span>✈️</span>
          <span>📍</span>
        </div>
      </div>

      {/* Popular Destinations */}
      <div className="home-section">
        <h2 className="home-section-title">POPULAR DESTINATION</h2>
        <div className="dest-grid">
          {filtered.map(dest => (
            <Link
              to={`/plan-trip?destination=${dest.name}`}
              className="dest-card"
              key={dest.name}
              style={{ backgroundImage: `url(${dest.photo})` }}
            >
              <div className="dest-card-overlay" />
              <span className="dest-card-name">{dest.name}</span>
            </Link>
          ))}
        </div>
      </div>

    </div>
  );
}

export default Home;
