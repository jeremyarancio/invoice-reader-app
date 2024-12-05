import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import InvoiceList from './components/Invoice/InvoiceList';
import UploadInvoice from './components/Invoice/UploadInvoice';
import Profile from './components/Profile/Profile';
import Login from './components/Auth/Login';
import RegisterUser from './components/Auth/Register';
import { queryClient } from './services/api';
import { QueryClientProvider } from '@tanstack/react-query';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Navbar />
        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<InvoiceList />} />
            <Route path="/upload" element={<UploadInvoice />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<RegisterUser />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;