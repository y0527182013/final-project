import { useLocation, useNavigate } from "react-router-dom";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state?.result;

  const handleBack = () => {
    navigate("/");
  };

  if (!result) {
    return (
      <div style={{ textAlign: "center", marginTop: "100px" }}>
        <h2>אין תוצאה להצגה</h2>
        <button onClick={handleBack}>חזרה לדף הבית</button>
      </div>
    );
  }

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>תוצאת ניתוח</h2>
      <pre>{JSON.stringify(result, null, 2)}</pre>
      <button onClick={handleBack} style={{ marginTop: "20px" }}>
        חזרה לדף הבית
      </button>
    </div>
  );
}

export default Result;
