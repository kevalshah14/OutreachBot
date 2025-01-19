import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FileInputPage from "./FileInputPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FileInputPage />} />
      </Routes>
    </Router>
  );
}

export default App;
