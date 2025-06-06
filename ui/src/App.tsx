import { BrowserRouter, Routes, Route } from "react-router-dom";
import Invoices from "@/pages/Invoices";
import Clients from "@/pages/Clients";
import SidebarLayout from "./components/SidebarLayout";
import AddInvoice from "@/pages/AddInvoice";
import AddClient from "@/pages/AddClient";
import SignIn from "@/pages/SignIn";
import SignUp from "@/pages/SignUp";
import { AuthLayout } from "@/components/layouts/AuthLayout";
import PageNotFound from "@/pages/PageNotFound";
import UserProfile from "@/pages/UserProfile";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/services/api/main";

function App() {
    return (
        <>
            <QueryClientProvider client={queryClient}>
                <BrowserRouter>
                    <Routes>
                        <Route element={<AuthLayout />}>
                            <Route path="/signin" element={<SignIn />} />
                            <Route path="/signup" element={<SignUp />} />
                        </Route>
                        <Route element={<SidebarLayout />}>
                            <Route path="/invoices" element={<Invoices />} />
                            <Route
                                path="/invoices/add"
                                element={<AddInvoice />}
                            />
                            <Route path="/clients" element={<Clients />} />
                            <Route
                                path="/clients/add"
                                element={<AddClient />}
                            />
                            <Route path="/user" element={<UserProfile />} />
                        </Route>
                        <Route path="/*" element={<PageNotFound />} />
                    </Routes>
                </BrowserRouter>
            </QueryClientProvider>
        </>
    );
}

export default App;
