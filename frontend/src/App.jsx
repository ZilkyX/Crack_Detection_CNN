import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    const formData = new FormData();
    formData.append("file", selectedImage);
    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/predict",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResult(response.data);
      console.log(response.data);
    } catch (error) {
      setResult({ error: "Prediction failed. Please check the backend." });
    } finally {
      setLoading(false);
    }
  };

  return (
 
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        style={{
          textAlign: "center",
          padding: "2rem",
          border: "2px dashed #ccc",
          borderRadius: "12px",
          maxWidth: "600px",
          margin: "2rem auto",
        }}
      >
        <h2>Crack Detection</h2>
        <p>Drag and drop an image or click to upload</p>
        <input type="file" accept="image/*" onChange={handleFileChange} />

        {preview && (
          <div style={{ marginTop: "1rem" }}>
            <img src={preview} alt="preview" style={{ width: "300px" }} />
          </div>
        )}

        <button
          onClick={handleSubmit}
          style={{
            marginTop: "1rem",
            padding: "0.5rem 1rem",
            fontSize: "1rem",
          }}
        >
          {loading ? "Predicting..." : "Predict"}
        </button>

        {result && (
          <div style={{ marginTop: "1rem" }}>
            {result.error ? (
              <p style={{ color: "red" }}>{result.error}</p>
            ) : (
              <>
                <h3>Result:</h3>
                <p>
                  Class: <strong>{result.class}</strong>
                </p>
                <p>
                  Confidence:{" "}
                  <strong>{(result.confidence * 100).toFixed(2)}%</strong>
                </p>
              </>
            )}
          </div>
        )}
      </div>
  );
}

export default App;
