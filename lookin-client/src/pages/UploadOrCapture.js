// import React, { useState, useRef } from "react";
// import Webcam from "react-webcam";
// import { useNavigate } from "react-router-dom";
// import './UploadOrCapture.css';

// function CaptureOrUpload() {
//   const [mode, setMode] = useState(null);
//   const [previewSrc, setPreviewSrc] = useState(null);
//   const webcamRef = useRef(null);
//   const navigate = useNavigate();

//   const handleCapture = async () => {
//     const imageSrc = webcamRef.current.getScreenshot();
//     if (imageSrc) {
//       setPreviewSrc(imageSrc);
//       await sendImage(imageSrc);
//     } else {
//       alert("לא הצלחנו לצלם תמונה");
//     }
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       const reader = new FileReader();
//       reader.onloadend = () => {
//         setPreviewSrc(reader.result);
//       };
//       reader.readAsDataURL(file);
//       sendImage(file);
//     }
//   };

//   const sendImage = async (imageData) => {
//     try {
//       let file;

//       if (typeof imageData === "string") {
//         const base64Data = imageData.split(',')[1];
//         const byteCharacters = atob(base64Data);
//         const byteNumbers = new Array(byteCharacters.length)
//           .fill()
//           .map((_, i) => byteCharacters.charCodeAt(i));
//         const byteArray = new Uint8Array(byteNumbers);
//         const blob = new Blob([byteArray], { type: 'image/jpeg' });
//         file = new File([blob], "photo.jpg", { type: "image/jpeg" });
//       } else {
//         file = imageData;
//       }

//       const formData = new FormData();
//       formData.append("file", file);

//       //localhost:8001-כתובת מקומית של השרת שלי
//       const response = await fetch("https://lookin-58h4.onrender.com/validate", {
//         method: "POST",
//         body: formData,
//         mode: "cors"
//       });

//       if (response.ok) {
//         const data = await response.json();
//         console.log("Response data:", data);
//         navigate('/result', {
//           state: { result: data.result }
//         });
//       } else {
//         const text = await response.text();
//         alert("שגיאה מהשרת: " + text);
//       }
//     } catch (err) {
//       console.error("שגיאה בשליחת התמונה לשרת:", err);
//       alert("שגיאה בשליחת התמונה לשרת: " + err.message);
//     }
//   };

//   return (
//     <div className="upload-container">
//       <div className="upload-card">
//         {!mode && (
//           <>
//             <h2>בחרי אפשרות</h2>
//             <button className="b" onClick={() => setMode("camera")}>צילום מצלמה</button>
//             <button className="b" onClick={() => setMode("upload")}>העלאת תמונה</button>
//           </>
//         )}

//         {mode === "camera" && (
//           <div className="upload-camera">
//             <Webcam
//               ref={webcamRef}
//               screenshotFormat="image/jpeg"
//               width={300}
//               height={240}
//             />
//             <br />
//             <button className="b" onClick={handleCapture}>צלמי ושלחי</button>
//           </div>
//         )}

//         {mode === "upload" && (
//           <div className="upload-upload">
//             <label className="custom-file-upload">
//               <input type="file" accept="image/*" onChange={handleFileChange} />
//               בחרי תמונה
//             </label>
//           </div>
//         )}

//         {previewSrc && (
//           <div className="preview-image">
//             <h4>תצוגה מקדימה:</h4>
//             <img src={previewSrc} alt="preview" />
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default CaptureOrUpload;
import React, { useState, useRef, useEffect } from "react";
import Webcam from "react-webcam";
import { useNavigate } from "react-router-dom";
import imageCompression from "browser-image-compression";
import './UploadOrCapture.css';

function CaptureOrUpload() {
  const [mode, setMode] = useState(null);
  const [previewSrc, setPreviewSrc] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  // 🔔 מעיר את השרת ברגע שהמסך נטען
  useEffect(() => {
    fetch("https://lookin-58h4.onrender.com/validate", {
      method: "GET",
      mode: "cors"
    })
      .then(() => console.log("🔔 שרת התעורר"))
      .catch((err) => console.warn("⚠️ שגיאה ב־ping:", err));
  }, []);

  const handleCapture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      setPreviewSrc(imageSrc);
      await sendImage(imageSrc);
    } else {
      alert("לא הצלחנו לצלם תמונה");
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreviewSrc(URL.createObjectURL(file));
      await sendImage(file);
    }
  };

  const sendImage = async (imageData) => {
    setIsLoading(true);
    try {
      let file;

      if (typeof imageData === "string") {
        // base64 → File
        const base64Data = imageData.split(',')[1];
        const byteCharacters = atob(base64Data);
        const byteNumbers = new Array(byteCharacters.length)
          .fill()
          .map((_, i) => byteCharacters.charCodeAt(i));
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'image/jpeg' });
        file = new File([blob], "photo.jpg", { type: "image/jpeg" });
      } else {
        file = imageData;
      }

      // 📦 דחיסת תמונה לפני שליחה
      const compressedFile = await imageCompression(file, {
        maxSizeMB: 0.3,
        maxWidthOrHeight: 800,
        useWebWorker: true
      });

      const formData = new FormData();
      formData.append("file", compressedFile);

      const response = await fetch("https://lookin-58h4.onrender.com/validate", {
        method: "POST",
        body: formData,
        mode: "cors"
      });

      if (response.ok) {
        const data = await response.json();
        navigate('/result', { state: { result: data.result } });
      } else {
        const text = await response.text();
        alert("שגיאה מהשרת: " + text);
      }
    } catch (err) {
      console.error("שגיאה בשליחת התמונה לשרת:", err);
      alert("שגיאה בשליחת התמונה לשרת: " + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        {!mode && (
          <>
            <h2>בחרי אפשרות</h2>
            <button className="b" onClick={() => setMode("camera")}>צילום מצלמה</button>
            <button className="b" onClick={() => setMode("upload")}>העלאת תמונה</button>
          </>
        )}

        {mode === "camera" && (
          <div className="upload-camera">
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              screenshotQuality={0.7}
              width={300}
              height={240}
            />
            <br />
            <button className="b" onClick={handleCapture} disabled={isLoading}>
              {isLoading ? "שולח..." : "צלמי ושלחי"}
            </button>
          </div>
        )}

        {mode === "upload" && (
          <div className="upload-upload">
            <label className="custom-file-upload">
              <input type="file" accept="image/jpeg,image/png" onChange={handleFileChange} disabled={isLoading} />
              בחרי תמונה
            </label>
          </div>
        )}

        {isLoading && (
          <div className="spinner">⏳ שולח תמונה... אנא המתיני</div>
        )}

        {previewSrc && (
          <div className="preview-image">
            <h4>תצוגה מקדימה:</h4>
            <img src={previewSrc} alt="preview" />
          </div>
        )}
      </div>
    </div>
  );
}

export default CaptureOrUpload;
