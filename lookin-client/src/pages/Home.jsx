// // Home.jsx
// import { useNavigate } from 'react-router-dom';
// import logo from '../assets/logo.png';
// import './Home.css'; // נוסיף CSS חיצוני
// function Home() {
//   const navigate = useNavigate();
//   const handleClick = () => {
//     navigate('/upload');
//   };
//   return (
//     <div className="home-container">
//       <img src={logo} alt="לוגו" className="home-logo" />
//       <button className="home-button" onClick={handleClick}>התחל אבחון</button>
//     </div>
//   );
// }
// export default Home;

import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import './Home.css';

function Home() {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate('/upload');
  };

  return (
    <div className="home-container">
      <div className="home-card">
        <img src={logo} alt="לוגו" className="home-logo" />
        <button className="home-button" onClick={handleClick}>
          התחל אבחון
        </button>
      </div>
    </div>
  );
}

export default Home;
