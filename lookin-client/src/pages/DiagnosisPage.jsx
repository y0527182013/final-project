import React, { useRef, useState } from 'react';
import './DiagnosisPage.css';
import axios from 'axios';

function DiagnosisPage() {
  const fileInputRef = useRef(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setResult('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data.result || 'נותח בהצלחה!');
    } catch (error) {
      console.error('שגיאה בשליחה לשרת:', error);
      setResult('אירעה שגיאה');
    }

    setLoading(false);
  };

  return (
    <div className="diagnosis-container">
      <h2>נא להעלות תמונה או לצלם</h2>
      <button
        className="upload-button"
        onClick={() => fileInputRef.current.click()}
        disabled={loading}
      >
        {loading ? 'שולח...' : 'העלאת תמונה / צילום'}
      </button>
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        capture="environment"
      />
      {result && <p className="result">{result}</p>}
    </div>
  );
}

export default DiagnosisPage;
