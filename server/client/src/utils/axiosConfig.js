import axios from 'axios';

const instance = axios.create({
  baseURL: `http://${process.env.REACT_APP_IP_ADDRESS}:3000`,
});

instance.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`;

export default instance;
