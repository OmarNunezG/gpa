import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginScreen from './screens/LoginScreen';
import AccountsScreen from './screens/AccountsScreen';
import TransactionsScreen from './screens/TransactionsScreen';

function App() {
  return (
    <Router>
      <main className="py-3">
        <Routes>
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/accounts" element={<AccountsScreen />} />
          <Route path="/transactions" element={<TransactionsScreen />} />
          <Route
            path="/transactions/:accountNumber"
            element={<TransactionsScreen />}
          />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
