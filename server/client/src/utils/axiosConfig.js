import axios from 'axios';

const instance = axios.create({
  baseURL: `http://${process.env.REACT_APP_IP_ADDRESS}:3000`,
});

export default instance;
