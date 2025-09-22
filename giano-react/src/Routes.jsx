// src/Routes.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";
import Records from "./components/Records";
import Mobile from "./components/mobile";

import QRCodeDisplay from "./components/displayQr"; // Correct import for displayQr

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<QRCodeDisplay />} />
      <Route path="/records" element={<Records />} />  {/* changed path */}

      <Route path="/mobile/:token" element={<Mobile />} />
    </Routes>
  );
};

export default AppRoutes;

