// CaptureOrUpload.js
import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import { useNavigate } from "react-router-dom";
console.log("CaptureOrUpload loaded");
function CaptureOrUpload() {
  const [mode, setMode] = useState(null);
  const webcamRef = useRef(null);
  const navigate = useNavigate();
  const handleCapture = async () => {
    const imageSrc = webcamRef.current.getScreenshot(); // jpeg
    if (imageSrc) {
      sendImage(imageSrc);
    } else {
      alert("לא הצלחנו לצלם תמונה");
    }
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    sendImage(file);
  };
  const sendImage = async (imageData) => {
  try {
    let file;
    if (typeof imageData === "string") {
      // זה base64 מהמצלמה
      const base64Data = imageData.split(',')[1];
      const byteCharacters = atob(base64Data);
      const byteNumbers = new Array(byteCharacters.length).fill().map((_, i) => byteCharacters.charCodeAt(i));
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'image/jpeg' });
      file = new File([blob], "photo.jpg", { type: "image/jpeg" });
    } else {
      // זה קובץ מהעלאה
      file = imageData;
    }
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("http://localhost:8001/validate", {
      method: "POST",
      body: formData,
    });
    const text = await response.text();
    if (response.ok) {
      const data = JSON.parse(text);
      navigate("/result", { state: { result: data.result } });
    } else {
      alert("שגיאה מהשרת: " + text);
    }
  } catch (err) {
    console.error("שגיאה בשליחת התמונה לשרת:", err);
    alert("שגיאה בשליחת התמונה לשרת: " + err.message);
  }
};
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      {!mode && (
        <>
          <h2>בחרי אפשרות</h2>
          <button className="b" conClick={() => setMode("camera")}>צילום מצלמה</button>
          <button className="b" onClick={() => setMode("upload")}>העלאת תמונה</button>
        </>
      )}
      {mode === "camera" && (
        <div>
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width={640}
            height={480}
          />
          <br />
          <button className="b" onClick={handleCapture}>צלמי ושלחי</button>
        </div>
      )}
      {mode === "upload" && (
        <div>
          <input type="file" accept="image/*" onChange={handleFileChange} />
        </div>
      )}
    </div>
  );
}
export default CaptureOrUpload;