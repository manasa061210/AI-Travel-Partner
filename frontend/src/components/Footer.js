import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-brand">
          <div className="footer-logo">
            <span>✈</span> TravelPartner
          </div>
          <p className="footer-tagline">Your AI-Powered Travel Companion.<br />Plan smarter. Travel better.</p>
          <div className="footer-social">
            <span>🌐</span><span>📘</span><span>🐦</span><span>📸</span>
          </div>
        </div>

        <div className="footer-links">
          <div className="footer-col">
            <h4>Explore</h4>
            <Link to="/destinations">Destinations</Link>
            <Link to="/plan-trip">Plan a Trip</Link>
            <Link to="/">Popular Routes</Link>
            <Link to="/">Travel Guides</Link>
          </div>
          <div className="footer-col">
            <h4>Account</h4>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/profile">My Profile</Link>
          </div>
          <div className="footer-col">
            <h4>Company</h4>
            <Link to="/">About Us</Link>
            <Link to="/">Contact</Link>
            <Link to="/">Privacy Policy</Link>
            <Link to="/">Terms of Service</Link>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>AI Enhanced Travel Companion</p>
      </div>
    </footer>
  );
}

export default Footer;
