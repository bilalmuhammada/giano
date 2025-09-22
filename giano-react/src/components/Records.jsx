import React, { useEffect, useState } from "react";
import axios from "axios";

const Records = () => {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/attendance/records/")
      .then((res) => {
        setRecords(res.data.records); // <-- Correct
      })
      .catch((err) => console.error("Error fetching records:", err));
  }, []);

  return (
    <div className="p-6 bg-white shadow-md rounded-xl">
      <h2 className="text-xl font-bold mb-4">Attendance Records</h2>

      {records.length === 0 ? (
        <p className="text-gray-500">No records found</p>
      ) : (
        <ul className="space-y-3">
          {records.map((rec) => (
            <li
              key={rec.id}
              className="p-4 border rounded-lg bg-gray-50 hover:bg-gray-100 transition"
            >
              <div className="flex justify-between items-center">
                <span className="font-medium text-gray-800">
                  {rec.user__username}
                </span>
                <span className="text-sm text-gray-500">
                  {new Date(rec.timestamp).toLocaleString()}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Records;
