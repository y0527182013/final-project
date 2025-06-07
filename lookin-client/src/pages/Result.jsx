// import { useLocation, useNavigate } from "react-router-dom";
// import { useState } from "react";
// import './Result.css';

// function Result() {
//   const location = useLocation();
//   const navigate = useNavigate();
//   const result = location.state?.result;

//   const [showGuidance, setShowGuidance] = useState(false);

//   const handleBack = () => {
//     navigate("/");
//   };

//   if (!result) {
//     return (
//       <div className="result-container">
//         <div className="result-card">
//           <h2>אין תוצאה להצגה</h2>
//           <button className="home-button" onClick={handleBack}>חזרה לדף הבית</button>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="result-container">
//       <div className="result-card">
//         <h2>אבחון אישי</h2>
//         <p className="result-text">{result.description}</p>

//         {!showGuidance && (
//           <button className="home-button" onClick={() => setShowGuidance(true)}>
//             הצגת הכוונה תעסוקתית
//           </button>
//         )}

//         {showGuidance && (
//           <div className="guidance-section">
//             <h3>הכוונה תעסוקתית</h3>
//             <p className="result-text">{result.career}</p>
//           </div>
//         )}

//         <button className="back-button" onClick={handleBack}>
//           חזרה לדף הבית
//         </button>
//       </div>
//     </div>
//   );
// }

// export default Result;

//////////////////

// import React from 'react';
// import { useLocation, useNavigate } from 'react-router-dom';

// function Result() {
//   const location = useLocation();
//   const navigate = useNavigate();

//   const result = location.state?.result;

//   if (!result) {
//     return (
//       <div>
//         <h2>אין תוצאה להצגה</h2>
//         <button onClick={() => navigate('/')}>חזרה לדף הבית</button>
//       </div>
//     );
//   }

//   return (
//     <div style={{ padding: '20px', direction: 'rtl' }}>
//       <h2>תוצאה מהשרת:</h2>
//       <pre style={{
//         background: '#f5f5f5',
//         padding: '10px',
//         borderRadius: '5px',
//         overflowX: 'auto'
//       }}>
//         {JSON.stringify(result, null, 2)}
//       </pre>
//       <button onClick={() => navigate('/')}>התחלה מחדש</button>
//     </div>
//   );
// }

// export default Result;

////////////////////
import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import './Result.css';

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  // הנתונים מועברים דרך location.state.result
  const result = location.state?.result; 
  console.log(location.state?.result)
  const [showGuidance, setShowGuidance] = useState(false);

  const handleBack = () => {
    navigate("/");
  };

  if (!result) {
    return (
      <div className="result-container">
        <div className="result-card">
          <h2>אין תוצאה להצגה</h2>
          <button className="home-button" onClick={handleBack}>חזרה לדף הבית</button>
        </div>
      </div>
    );
  }

  return (
    <div className="result-container">
      <div className="result-card">
        <h2>אבחון אישי</h2>
        {/* שימוש ב-result.description עבור התיאור */}
        <p className="result-text">{result.description}</p>

        {!showGuidance && (
          <button className="home-button" onClick={() => setShowGuidance(true)}>
            הצגת הכוונה תעסוקתית
          </button>
        )}

        {showGuidance && (
          <div className="guidance-section">
            <h3>הכוונה תעסוקתית</h3>
            {/* שינוי מ-result.career ל-result.career_guidance */}
            <p className="result-text">{result.career_guidance}</p>
          </div>
        )}

        <button className="back-button" onClick={handleBack}>
          חזרה לדף הבית
        </button>
      </div>
    </div>
  );
}

export default Result;