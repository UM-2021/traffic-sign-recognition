import React, { useState, createContext, useContext } from 'react';
import instance from '../utils/axiosConfig';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const sessionStorageValue = JSON.parse(sessionStorage.getItem('loggedIn'));
  const [authed, setAuthed] = useState(sessionStorageValue);

  const login = async (email, password) => {
    try {
      const res = await instance.post('/api/users/login', {
        email,
        password,
      });
      sessionStorage.setItem('loggedIn', 'true');
      localStorage.setItem('token', res.data.token);
      await sleep(1000);

      setAuthed(true);
      return res;
    } catch (e) {
      sessionStorage.setItem('loggedIn', 'false');
      setAuthed(false);
      return e.response;
    }
  };

  const logout = async () => {
    await instance('/api/users/logout', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
    sessionStorage.setItem('loggedIn', 'false');
    localStorage.clear();
    setAuthed(false);
  };

  return (
    <AuthContext.Provider value={{ authed, setAuthed, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
