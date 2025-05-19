import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import './Home.css'; // נוסיף CSS חיצוני
function Home() {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate('/upload');
  };
  return (
    <div className="home-container">
      <img src={logo} alt="לוגו" className="home-logo" />
      <button className="home-button" onClick={handleClick}>התחל אבחון</button>
    </div>
  );
}
export default Home;