import axios from "axios";

export default axios.create({
  baseURL: API_URL,
  withCredentials: true,
});
