// App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FileInputPage from "./FileInputPage";
import FileRenderPage from "./FileRenderPage";
import "./index.css";

function App() {
  return (
    <Router>
      <Routes>
        {/* File Input Page (/) */}
        <Route path="/" element={<FileInputPage />} />

        {/* File Render/Preview Page (/render) */}
        <Route path="/render" element={<FileRenderPage />} />
      </Routes>
    </Router>
  );
}

export default App;
