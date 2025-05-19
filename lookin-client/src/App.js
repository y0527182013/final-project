import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import UploadOrCapture from './pages/UploadOrCapture';
import Result from './pages/Result'; 

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/upload" element={<UploadOrCapture />} />
      <Route path="/result" element={<Result />} />
    </Routes>
  );
}
export default App;
