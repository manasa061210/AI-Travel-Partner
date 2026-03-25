import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin, user, logout } = useAuth();

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    logout();
    navigate('/');
    setDropdownOpen(false);
    setMenuOpen(false);
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            <span className="brand-icon">✈</span>
            <span className="brand-text">AI-Travel<span className="brand-accent">Partner</span></span>
          </Link>

          <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
            <span /><span /><span />
          </button>

          <ul className={`navbar-links ${menuOpen ? 'open' : ''}`}>
            <li><Link to="/" className={isActive('/') ? 'active' : ''} onClick={() => setMenuOpen(false)}>Home</Link></li>
            <li><Link to="/destinations" className={isActive('/destinations') ? 'active' : ''} onClick={() => setMenuOpen(false)}>Explore</Link></li>
            <li><Link to="/food" className={isActive('/food') ? 'active' : ''} onClick={() => setMenuOpen(false)}>Food</Link></li>
            {isAuthenticated && (
              <li><Link to="/plan-trip" className={isActive('/plan-trip') ? 'active' : ''} onClick={() => setMenuOpen(false)}>Plan Trip</Link></li>
            )}
            {isAuthenticated && (
              <li><Link to="/dashboard" className={isActive('/dashboard') ? 'active' : ''} onClick={() => setMenuOpen(false)}>Bookings</Link></li>
            )}
            {isAdmin && (
              <li><Link to="/admin" className={isActive('/admin') ? 'active' : ''} onClick={() => setMenuOpen(false)}>Admin</Link></li>
            )}
          </ul>

          <div className={`navbar-auth ${menuOpen ? 'open' : ''}`}>
            {isAuthenticated ? (
              <div className="user-menu">
                <button className="user-btn" onClick={() => setDropdownOpen(!dropdownOpen)}>
                  <span className="user-avatar">{user?.name?.charAt(0).toUpperCase()}</span>
                  <span className="user-name">{user?.name?.split(' ')[0]}</span>
                  <span className="chevron">▾</span>
                </button>
                {dropdownOpen && (
                  <div className="dropdown">
                    <Link to="/dashboard" onClick={() => setDropdownOpen(false)}>📊 Dashboard</Link>
                    <Link to="/profile" onClick={() => setDropdownOpen(false)}>👤 Profile</Link>
                    {isAdmin && <Link to="/admin" onClick={() => setDropdownOpen(false)}>⚙️ Admin</Link>}
                    <hr />
                    <button onClick={handleLogout}>🚪 Logout</button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link to="/login" className="btn-nav-outline" onClick={() => setMenuOpen(false)}>Login</Link>
                <Link to="/register" className="btn-nav-filled" onClick={() => setMenuOpen(false)}>Get Started</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Bottom Navigation Bar (mobile) */}
      <nav className="bottom-nav">
        <div className="bottom-nav-inner">
          <Link to="/" className={`bnav-item ${isActive('/') ? 'active' : ''}`}>
            <span className="bnav-icon">🏠</span>Home
          </Link>
          <Link to="/destinations" className={`bnav-item ${isActive('/destinations') ? 'active' : ''}`}>
            <span className="bnav-icon">🔍</span>Explore
          </Link>
          <Link to="/food" className={`bnav-item ${isActive('/food') ? 'active' : ''}`}>
            <span className="bnav-icon">🍽️</span>Food
          </Link>
          <Link to="/plan-trip" className={`bnav-item ${isActive('/plan-trip') ? 'active' : ''}`}>
            <span className="bnav-icon">🗺️</span>Plan
          </Link>
          {isAuthenticated ? (
            <Link to="/dashboard" className={`bnav-item ${isActive('/dashboard') ? 'active' : ''}`}>
              <span className="bnav-icon">📋</span>Trips
            </Link>
          ) : (
            <Link to="/login" className={`bnav-item ${isActive('/login') ? 'active' : ''}`}>
              <span className="bnav-icon">📋</span>Trips
            </Link>
          )}
          <Link to="/profile" className={`bnav-item ${isActive('/profile') ? 'active' : ''}`}>
            <span className="bnav-icon">👤</span>Profile
          </Link>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
