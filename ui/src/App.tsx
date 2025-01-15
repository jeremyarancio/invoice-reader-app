import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./common/Navbar";
import InvoiceList from "./pages/invoices/components/InvoiceList";
import ClientList from "./pages/clients/components/ClientList";
import UploadInvoice from "./pages/invoices/components/UploadInvoice";
import Profile from "./pages/profile/Profile";
import Login from "./pages/login/Login";
import RegisterUser from "./pages/login/Register";
import { queryClient } from "./services/api";
import { QueryClientProvider } from "@tanstack/react-query";
import ClientForm from "./pages/clients/components/ClientForm";

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <Router>
                <Navbar />
                <div className="container mt-4">
                    <Routes>
                        <Route path="/" element={<InvoiceList />} />
                        <Route path="/clients" element={<ClientList />} />
                        <Route path="/upload" element={<UploadInvoice />} />
                        <Route path="/clientform" element={<ClientForm />} />
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
