import React, { useState, createContext, useContext } from 'react';
import instance from '../utils/axiosConfig';

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
      setAuthed(true);
      return res;
    } catch (e) {
      sessionStorage.setItem('loggedIn', 'false');
      setAuthed(false);
      return e.response;
    }
  };

  const logout = async () => {
    await instance('/api/users/logout');
    sessionStorage.setItem('loggedIn', 'false');
    setAuthed(false);
  };

  return (
    <AuthContext.Provider value={{ authed, setAuthed, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
