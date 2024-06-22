import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import OverpaidPlayers from './OverpaidPlayers';
import HighestPaidPlayers from './HighestPaidPlayers';
import UnderpaidPlayers from './UnderpaidPlayers';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 text-gray-900">
        <header className="bg-blue-600 text-white shadow-lg">
          <div className="container mx-auto py-4 px-6">
            <h1 className="text-3xl font-bold">NBA Player Statistics</h1>
          </div>
        </header>
        <nav className="bg-white shadow-md">
          <div className="container mx-auto px-6">
            <ul className="flex space-x-4 py-4">
              <li>
                <Link to="/overpaid" className="text-blue-600 hover:text-blue-800 font-medium">Most Overpaid Players</Link>
              </li>
              <li>
                <Link to="/highest-paid" className="text-blue-600 hover:text-blue-800 font-medium">Highest Paid Players</Link>
              </li>
              <li>
                <Link to="/underpaid" className="text-blue-600 hover:text-blue-800 font-medium">Most Underpaid Players</Link>
              </li>
            </ul>
          </div>
        </nav>
        <main className="container mx-auto mt-8 px-6">
          <Routes>
            <Route path="/overpaid" element={<OverpaidPlayers />} />
            <Route path="/highest-paid" element={<HighestPaidPlayers />} />
            <Route path="/underpaid" element={<UnderpaidPlayers />} />
            <Route path="/" element={<h2 className="text-2xl font-semibold">Welcome to NBA Player Statistics</h2>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;