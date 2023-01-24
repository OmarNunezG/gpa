import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginScreen from './screens/LoginScreen';

function App() {
  return (
    <Router>
      <main className="py-3">
        <Routes>
          <Route path="/login" element={<LoginScreen />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
