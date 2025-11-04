import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

let token = null;

export const setToken = (t) => {
  token = t;
  API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};

// Auth
export const register = (data) => API.post("/auth/register", data);
export const login = (data) => API.post("/auth/login", new URLSearchParams(data));
export const me = () => API.get("/auth/me");

// Battery
export const listBatteries = (params) => API.get("/battery", { params });
export const createBattery = (data) => API.post("/battery", data);
export const updateBattery = (id, data) => API.put(`/battery/${id}`, data);
export const deleteBattery = (id) => API.delete(`/battery/${id}`);

// Devices
export const listDevices = (params) => API.get("/devices", { params });
export const createDevice = (data) => API.post("/devices", data);
export const updateDevice = (id, data) => API.put(`/devices/${id}`, data);
export const deleteDevice = (id) => API.delete(`/devices/${id}`);
export const addBatteriesToDevice = (device_id, batteries) =>
  API.post(`/devices/${device_id}/battaries`, batteries);
export const deleteBatteryByDevice = (device_id, battery_id) =>
  API.delete(`/devices/${device_id}/battaries/${battery_id}`);
