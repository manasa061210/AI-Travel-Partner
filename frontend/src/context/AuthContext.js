import React, { createContext, useContext, useState, useCallback } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

const API_BASE = 'http://localhost:5000';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('travel_user')); } catch { return null; }
  });
  const [token, setToken] = useState(() => localStorage.getItem('travel_token'));

  const login = useCallback(async (email, password) => {
    const res = await axios.post(`${API_BASE}/api/auth/login`, { email, password });
    const { token: t, user: u } = res.data.data;
    localStorage.setItem('travel_token', t);
    localStorage.setItem('travel_user', JSON.stringify(u));
    setToken(t);
    setUser(u);
    return u;
  }, []);

  const register = useCallback(async (data) => {
    const res = await axios.post(`${API_BASE}/api/auth/register`, data);
    const { token: t, user: u } = res.data.data;
    localStorage.setItem('travel_token', t);
    localStorage.setItem('travel_user', JSON.stringify(u));
    setToken(t);
    setUser(u);
    return u;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('travel_token');
    localStorage.removeItem('travel_user');
    setToken(null);
    setUser(null);
  }, []);

  const updateUser = useCallback((u) => {
    localStorage.setItem('travel_user', JSON.stringify(u));
    setUser(u);
  }, []);

  return (
    <AuthContext.Provider value={{
      user, token,
      isAuthenticated: !!token,
      isAdmin: user?.role === 'admin',
      login, register, logout, updateUser,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
