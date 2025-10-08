import { BrowserRouter, Routes, Route } from "react-router-dom";
import Invoices from "@/pages/Invoices";
import Clients from "@/pages/Clients";
import SidebarLayout from "@/components/SidebarLayout";
import AddInvoice from "@/pages/AddInvoice";
import AddClient from "@/pages/AddClient";
import SignIn from "@/pages/SignIn";
import SignUp from "@/pages/SignUp";
import { AuthLayout } from "@/components/layouts/AuthLayout";
import PageNotFound from "@/pages/PageNotFound";
import UserProfile from "@/pages/UserProfile";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/services/api/main";
import ProtectedRoute from "@/components/ProtectedRoute"; // Import the ProtectedRoute
import AuthProvider from "@/components/AuthProvider";
import ViewInvoice from "@/pages/ViewInvoice";
import ViewClient from "@/pages/ViewClient";
import { AlertProvider } from "@/contexts/AlertContext";
import AppAlert from "@/components/AppAlert";

function App() {
    return (
        <>
            <QueryClientProvider client={queryClient}>
                <AuthProvider>
                    <AlertProvider>
                        <BrowserRouter>
                            <Routes>
                                <Route element={<AuthLayout />}>
                                    <Route path="/signin" element={<SignIn />} />
                                    <Route path="/signup" element={<SignUp />} />
                                </Route>
                                <Route element={<ProtectedRoute />}>
                                    <Route element={<SidebarLayout />}>
                                        <Route path="/" element={<Invoices />} />
                                        <Route
                                            path="/invoices"
                                            element={<Invoices />}
                                        />
                                        <Route
                                            path="/invoices/add"
                                            element={<AddInvoice />}
                                        />
                                        <Route
                                            path="/invoices/:invoiceId"
                                            element={<ViewInvoice />}
                                        />
                                        <Route
                                            path="/clients"
                                            element={<Clients />}
                                        />
                                        <Route
                                            path="/clients/add"
                                            element={<AddClient />}
                                        />
                                        <Route
                                            path="/clients/:clientId"
                                            element={<ViewClient />}
                                        />
                                        <Route
                                            path="/user"
                                            element={<UserProfile />}
                                        />
                                        <Route
                                            path="/*"
                                            element={<PageNotFound />}
                                        />
                                    </Route>
                                </Route>
                            </Routes>
                        </BrowserRouter>
                        <AppAlert />
                    </AlertProvider>
                </AuthProvider>
            </QueryClientProvider>
        </>
    );
}

export default App;
