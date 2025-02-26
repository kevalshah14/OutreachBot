// FileRenderPage.jsx
import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import * as XLSX from "xlsx";

function FileRenderPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const [file, setFile] = useState(null);
  const [previewType, setPreviewType] = useState("");
  const [previewSrc, setPreviewSrc] = useState(null);
  const [sheetData, setSheetData] = useState([]);

  // Check if we got here with a file
  useEffect(() => {
    if (!location.state?.file) {
      navigate("/");
      return;
    }
    setFile(location.state.file);
  }, [location, navigate]);

  // Determine preview type and process file
  useEffect(() => {
    if (!file) return;

    const { type, name } = file;

    // IMAGE
    if (type.startsWith("image/")) {
      setPreviewType("image");
      setPreviewSrc(URL.createObjectURL(file));
    }
    // PDF
    else if (type === "application/pdf") {
      setPreviewType("pdf");
      setPreviewSrc(URL.createObjectURL(file));
    }
    // EXCEL
    else if (
      type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
      type === "application/vnd.ms-excel" ||
      name.endsWith(".xlsx") ||
      name.endsWith(".xls")
    ) {
      setPreviewType("excel");
      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        setSheetData(jsonData);
      };
      reader.readAsArrayBuffer(file);
    }
    // CSV
    else if (
      type === "text/csv" ||
      type === "application/csv" ||
      name.endsWith(".csv")
    ) {
      setPreviewType("excel"); // Reuse the same table preview
      const reader = new FileReader();
      reader.onload = (e) => {
        const csvData = e.target.result;
        const workbook = XLSX.read(csvData, { type: "string" });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        setSheetData(jsonData);
      };
      reader.readAsText(file);
    }
    // OTHER
    else {
      setPreviewType("other");
    }
  }, [file]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-800 p-4">
      <motion.div
        className="max-w-3xl w-full bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 text-white"
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 80, damping: 15 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">File Preview</h1>
          <button
            onClick={() => navigate("/")}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
          >
            Back
          </button>
        </div>

        {file && (
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-sm text-gray-300 break-all">
              <strong>File:</strong> {file.name}
            </p>

            {/* Image Preview */}
            {previewType === "image" && previewSrc && (
              <div className="flex justify-center">
                <img
                  src={previewSrc}
                  alt="Preview"
                  className="max-h-[30rem] object-contain rounded"
                />
              </div>
            )}

            {/* PDF Preview */}
            {previewType === "pdf" && previewSrc && (
              <iframe
                src={previewSrc}
                title="PDF Preview"
                className="w-full h-[30rem] rounded"
              />
            )}

            {/* Excel/CSV Preview */}
            {previewType === "excel" && (
              <div className="overflow-auto max-h-[30rem] bg-gray-100 rounded p-4 text-gray-800">
                <table className="min-w-full text-sm">
                  <tbody>
                    {sheetData.map((row, rowIndex) => (
                      <tr key={rowIndex} className="border-b last:border-none">
                        {row.map((cell, cellIndex) => (
                          <td
                            key={cellIndex}
                            className="p-2 border-r last:border-none"
                          >
                            {cell || ""}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Other Preview */}
            {previewType === "other" && (
              <p className="text-gray-200 italic">
                No preview available for this file type.
              </p>
            )}
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}

export default FileRenderPage;