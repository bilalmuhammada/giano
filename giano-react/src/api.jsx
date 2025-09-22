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


export const confirmAttendance = async (token, code) => {
  if (!token || !code) {
    return { success: false, message: "Token and code are required" };
  }

  // Get CSRF token from cookies
  const csrftoken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];

  try {
    const response = await axios.post(
      `${API_BASE}/confirm/${token}/`,
      { code },
      {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken, // Include CSRF token
        },
        withCredentials: true, // Ensure credentials (cookies) are sent
      }
    );

    return response.data;
  } catch (error) {
    console.error(
      "Error confirming attendance:",
      error.response ? error.response.data : error.message
    );

    return {
      success: false,
      message:
        (error.response && error.response.data?.message) ||
        "Failed to confirm attendance",
    };
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
