import { Inbox, User, Bug } from "lucide-react";

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
                                    <SidebarMenuButton asChild>
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
            <SidebarFooter className="flex-col space-y-2">
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton asChild>
                            <a
                                href="https://github.com/jeremyarancio/invoice-reader-app/issues/new?template=bug_report.yml"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <Bug />
                                <span>Report a Bug</span>
                            </a>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>

                <SidebarUser />
            </SidebarFooter>
        </Sidebar>
    );
}
