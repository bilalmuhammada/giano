import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function MobilePage() {
  const { token } = useParams();
  const [code, setCode] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/attendance/get_code/${token}/`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setCode(data.data.code); // use data.data.code per your API
          console.log("Fetched code:", data.data.code); // ✅ log here
        } else {
          console.log("Failed to fetch code:", data.message);
        }
      })
      .catch(err => {
        console.error("Error fetching code:", err);
      });
  }, [token]);

  return (
    <div className="p-4 text-center">
      <h1 className="text-xl font-bold">Your Code</h1>
      
      {code ? (
        <p className="text-3xl">{code}</p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
