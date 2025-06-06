import { BrowserRouter, Routes, Route } from "react-router-dom";
import Invoices from "@/pages/Invoices";
import Clients from "@/pages/Clients";
import SidebarLayout from "./components/SidebarLayout";
import AddInvoice from "@/pages/AddInvoice";
import AddClient from "@/pages/AddClient";
import SignIn from "@/pages/SignIn";
import SignUp from "@/pages/SignUp";
import { AuthLayout } from "./components/layouts/AuthLayout";
import PageNotFound from "./pages/PageNotFound";
import UserProfile from "./pages/UserProfile";

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route element={<AuthLayout />}>
                        <Route path="/signin" element={<SignIn />} />
                        <Route path="/signup" element={<SignUp />} />
                    </Route>
                    <Route element={<SidebarLayout />}>
                        <Route path="/invoices" element={<Invoices />} />
                        <Route path="/invoices/add" element={<AddInvoice />} />
                        <Route path="/clients" element={<Clients />} />
                        <Route path="/clients/add" element={<AddClient />} />
                        <Route path="/user" element={<UserProfile />} />
                    </Route>
                    <Route path="/*" element={<PageNotFound />} />
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;
