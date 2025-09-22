import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/attendance";

export const getQRCode = async () => {
  try {
    const response = await axios.get(`${API_BASE}/get_qr/`);
    return response.data.data;
  } catch (error) {
    console.error("Error fetching QR code:", error);
    return null;
  }
};

export const getStatus = async (token) => {
  try {
    const response = await axios.get(`${API_BASE}/status/${token}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching status:", error);
    return null;
  }
};

export const confirmAttendance = async (token) => {
  try {
    const response = await axios.post(`${API_BASE}/confirm/${token}/`);
    return response.data;
  } catch (error) {
    console.error("Error confirming attendance:", error);
    return null;
  }
};

export const getRecords = async () => {
  try {
    const response = await axios.get(`${API_BASE}/records/`);
    console.log(response);
    return response.data.data;
  } catch (error) {
    console.error("Error fetching records:", error);
    return [];
  }
};
