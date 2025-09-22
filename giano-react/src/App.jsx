// src/App.jsx
import './App.css'
import { BrowserRouter as Router } from "react-router-dom";
import AppRoutes from "./Routes";
import QRCodeDisplay from "./components/displayQr";
import Records from "./components/Records";
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold mb-6">Giano Attendance</h1>
      
      </div>
      <AppRoutes /> {/* This will render Home/Mobile/Records based on route */}
    </Router>
  )
}

export default App
