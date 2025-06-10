import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { useState } from "react";
import { Outlet } from "react-router-dom";

export default function SidebarLayout() {
    const [open, setOpen] = useState(true);

    return (
        <SidebarProvider open={open} onOpenChange={setOpen}>
            <AppSidebar />
            <SidebarInset>
                <main>
                    <SidebarTrigger className="sticky" />
                    <Outlet />
                </main>
            </SidebarInset>
        </SidebarProvider>
    );
}
