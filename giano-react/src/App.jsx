import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import QRCodeDisplay from "./components/displayQr";
import Records from './components/Records';
import Mobile from './components/mobile';
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">Giano Attendance</h1>
      <QRCodeDisplay />
      <Mobile />
      <Records />
    </div>
    </>
  )
}

export default App
