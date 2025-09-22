import React, { useState, useEffect } from "react";
import { getQRCode, getStatus, confirmAttendance } from "../api";

export default function QRCodeDisplay() {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState(null);

  const fetchQRCode = async () => {
    const response = await getQRCode();
    setData(response);
  };

  // Poll status every 3 seconds
  useEffect(() => {
    if (!data?.token) return;
    const interval = setInterval(async () => {
      const s = await getStatus(data.token);
      setStatus(s?.status);
    }, 3000);
    return () => clearInterval(interval);
  }, [data]);

  const handleConfirm = async (choice) => {
    await confirmAttendance(data.token);
    alert(`Attendance confirmed with choice: ${choice}`);
  };

  return (
    
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-100 to-purple-100 p-6">
          <div className="bg-white p-8 rounded-3xl shadow-2xl flex flex-col items-center space-y-6 w-full max-w-md">
            
            <h2 className="text-3xl font-extrabold text-gray-800">Giano Attendance</h2>
            <p className="text-gray-500 text-center">Scan the QR or select a numeric code to log your session.</p>
      
            {/* Generate QR Button */}
            <button
              onClick={fetchQRCode}
              className="w-full bg-blue-600 text-white font-semibold py-3 rounded-xl shadow-md hover:bg-blue-700 transform hover:-translate-y-1 transition-all duration-200"
            >
              Generate QR Code
            </button>
      
            {data && (
              <>
                {/* QR Code */}
                <div className="bg-gray-50 py-4 rounded-xl shadow-inner mt-4">
                  <img
                    src={`data:image/png;base64,${data.qr_base64}`}
                    alt="QR Code"
                    className="w-60 h-60"
                  />
                </div>
      
                {/* Status */}
                <p className="text-gray-700 font-medium mt-2">Status: {status || "Waiting"}</p>
      
                {/* Numeric choices */}
                <div className="grid grid-cols-3 gap-3 w-full mt-4">
                  {data.numeric_code_choices.map((choice) => (
                    <button
                      key={choice}
                      onClick={() => handleConfirm(choice)}
                      className="bg-purple-100 text-purple-700 py-2 rounded-xl font-medium hover:bg-purple-200 transition"
                    >
                      {choice}
                    </button>
                  ))}
                </div>
      
                {/* Mobile URL */}
                <a
                  href={data.mobile_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 font-medium underline mt-4 hover:text-blue-800"
                >
                  Open Mobile URL
                </a>
              </>
            )}
          </div>
        </div>
      );
      
}
