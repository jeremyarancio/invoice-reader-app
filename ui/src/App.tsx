import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "@/common/Navbar";
import InvoiceList from "@/pages/invoices/components/InvoiceList";
import ClientList from "@/pages/clients/components/ClientList";
import UploadInvoice from "@/pages/invoices/components/UploadInvoice";
import { queryClient } from "@/services/api";
import { QueryClientProvider } from "@tanstack/react-query";
import ClientForm from "@/pages/clients/components/ClientForm";
import ProtectedRoute from "./common/components/ProtectedRoute";
import SignIn from "./pages/auth/SignIn";
import SignUp from "./pages/auth/SignUp";

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <Router>
                <Navbar />
                <div className="container mt-4">
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <ProtectedRoute>
                                    <InvoiceList />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/clients"
                            element={
                                <ProtectedRoute>
                                    <ClientList />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/upload"
                            element={
                                <ProtectedRoute>
                                    <UploadInvoice />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/clientform"
                            element={
                                <ProtectedRoute>
                                    <ClientForm />
                                </ProtectedRoute>
                            }
                        />
                        <Route path="/signin" element={<SignIn />} />
                        <Route path="/signup" element={<SignUp />} />
                    </Routes>
                </div>
            </Router>
        </QueryClientProvider>
    );
}

export default App;
