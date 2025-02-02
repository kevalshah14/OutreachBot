// FileInputPage.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

function FileInputPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);

  // Handle file selection from <input />
  const handleFileChange = (e) => {
    if (e.target.files?.[0]) {
      setFile(e.target.files[0]);
    }
  };

  // Handle drag & drop
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };
  const handleDragLeave = () => {
    setIsDragOver(false);
  };
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files?.[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  // Navigate to /render, passing the file object
  const goToRenderPage = () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }
    navigate("/render", { state: { file } });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-800 p-4">
      <motion.div
        className="max-w-lg w-full bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 text-white"
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 80, damping: 15 }}
      >
        <h1 className="text-3xl font-bold mb-6 text-center tracking-wide">
          Upload a File
        </h1>

        <div
          className={`relative border-2 border-dashed rounded-xl p-6 transition-colors 
            flex flex-col items-center justify-center 
            ${isDragOver ? "border-blue-400" : "border-white/40"} 
            mb-6`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <AnimatePresence>
            {!file && (
              <motion.div
                key="drop-hint"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center pointer-events-none"
              >
                <motion.svg
                  className="w-14 h-14 mb-3 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                  animate={{ y: [0, -4, 0] }}
                  transition={{
                    repeat: Infinity,
                    duration: 1.6,
                    ease: "easeInOut",
                  }}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3 15a4 4 0 010-8c.34 0 
                       .68.04 1 .12A5.002 5.002 0 0113 4
                       a5.002 5.002 0 014.9 3.63
                       A4.996 4.996 0 0123 12
                       a5 5 0 01-9 2H3z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 12v6m0 0l3-3m-3 3l-3-3"
                  />
                </motion.svg>
                <p className="text-base font-medium">
                  Drag &amp; Drop or Click to Select
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Hidden File Input */}
          <input
            type="file"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleFileChange}
          />

          {/* Selected File Name (if any) */}
          {file && (
            <p className="text-sm text-gray-200 font-semibold break-all pointer-events-none">
              {file.name}
            </p>
          )}
        </div>

        {/* "Next" button */}
        <button
          onClick={goToRenderPage}
          className="w-full py-2 bg-blue-600 hover:bg-blue-700 rounded-md font-semibold transition-colors"
        >
          Next
        </button>
      </motion.div>
    </div>
  );
}

export default FileInputPage;
