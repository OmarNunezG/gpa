import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginScreen from './screens/LoginScreen';
import AccountsScreen from './screens/AccountsScreen';

function App() {
  return (
    <Router>
      <main className="py-3">
        <Routes>
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/accounts" element={<AccountsScreen />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
