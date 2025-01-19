// src/FileInputPage.jsx
import React, { useState } from "react";
import { motion } from "framer-motion";

const containerVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 70,
      damping: 12,
      delay: 0.2,
    },
  },
};

const dropAreaVariants = {
  rest: {
    borderColor: "#e5e7eb", // gray-200
  },
  hover: {
    borderColor: "#3B82F6", // blue-500
    transition: {
      duration: 0.3,
    },
  },
};

const buttonVariants = {
  rest: {
    scale: 1,
    backgroundColor: "#3B82F6", // blue-500
    transition: { duration: 0.2 },
  },
  hover: {
    scale: 1.08,
    backgroundColor: "#2563EB", // blue-600
    transition: { duration: 0.2 },
  },
};

const FileInputPage = () => {
  const [fileName, setFileName] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      console.log("File selected:", file.name);
    }
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-screen
                 bg-gradient-to-r from-blue-400 via-pink-400 to-purple-500 p-4"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.h1
        className="text-4xl font-bold text-white mb-8"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.8, type: "tween" }}
      >
        Upload a File
      </motion.h1>

      <motion.label
        htmlFor="file-input"
        className="w-64 h-40 bg-white bg-opacity-30
                   rounded-xl border-4 border-dashed border-gray-300
                   flex flex-col items-center justify-center cursor-pointer
                   text-white transition-all"
        variants={dropAreaVariants}
        initial="rest"
        whileHover="hover"
        animate="rest"
      >
        <div className="flex flex-col items-center justify-center">
          <svg
            className="w-10 h-10 mb-2 text-white animate-bounce"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M4 16v1a2 2 0 002 2h3m4 0h3a2 2 0 002-2v-1M7 10l5-5m0 0l5 5m-5-5v12"
            />
          </svg>
          <p className="text-sm font-medium">Click or Drag &amp; Drop</p>
          {fileName && <p className="text-xs mt-2">Selected: {fileName}</p>}
        </div>
      </motion.label>

      <input
        id="file-input"
        type="file"
        onChange={handleFileChange}
        className="hidden"
      />

      <motion.button
        onClick={() => document.getElementById("file-input").click()}
        variants={buttonVariants}
        initial="rest"
        whileHover="hover"
        animate="rest"
        className="mt-6 px-6 py-3 text-white font-semibold
                   rounded-lg shadow-lg focus:outline-none"
      >
        Select File
      </motion.button>
    </motion.div>
  );
};

export default FileInputPage;
