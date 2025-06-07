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

//       const response = await fetch("http://localhost:8001/validate", {
//         method: "POST",
//         body: formData,
//         mode: "cors"
//       });

//       const text = await response.text();
//       if (response.ok) {
//      const data = await response.json();
//     navigate('/result', { state: { result: data } });
//       } else {
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
//////////////////

import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import { useNavigate } from "react-router-dom";
import './UploadOrCapture.css';

function CaptureOrUpload() {
  const [mode, setMode] = useState(null);
  const [previewSrc, setPreviewSrc] = useState(null);
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const handleCapture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      setPreviewSrc(imageSrc);
      await sendImage(imageSrc);
    } else {
      alert("לא הצלחנו לצלם תמונה");
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewSrc(reader.result);
      };
      reader.readAsDataURL(file);
      sendImage(file);
    }
  };

  const sendImage = async (imageData) => {
    try {
      let file;

      if (typeof imageData === "string") {
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

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8001/validate", {
        method: "POST",
        body: formData,
        mode: "cors"
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Response data:", data);
        navigate('/result', {
          state: { result: data.result }
        });
      } else {
        const text = await response.text();
        alert("שגיאה מהשרת: " + text);
      }
    } catch (err) {
      console.error("שגיאה בשליחת התמונה לשרת:", err);
      alert("שגיאה בשליחת התמונה לשרת: " + err.message);
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
              width={300}
              height={240}
            />
            <br />
            <button className="b" onClick={handleCapture}>צלמי ושלחי</button>
          </div>
        )}

        {mode === "upload" && (
          <div className="upload-upload">
            <label className="custom-file-upload">
              <input type="file" accept="image/*" onChange={handleFileChange} />
              בחרי תמונה
            </label>
          </div>
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
