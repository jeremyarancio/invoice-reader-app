import { Inbox, User } from "lucide-react";

import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";
import SidebarUser from "./SidebarUser";

// Menu items.
const items = [
    {
        title: "Invoices",
        url: "/invoices",
        icon: Inbox,
    },
    {
        title: "Clients",
        url: "/clients",
        icon: User,
    },
];

export function AppSidebar() {
    return (
        <Sidebar collapsible="icon">
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel className="mb-10 text-lg">
                        Invoice Manager
                    </SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {items.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton
                                        asChild
                                        className="text-lg font-semibold"
                                    >
                                        <a href={item.url}>
                                            <item.icon />
                                            <span>{item.title}</span>
                                        </a>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter className="flex space-x-4">
                <SidebarUser />
            </SidebarFooter>
        </Sidebar>
    );
}
