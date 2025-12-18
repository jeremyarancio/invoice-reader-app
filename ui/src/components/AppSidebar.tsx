import { Inbox, User, Bug, DollarSign, LayoutDashboard } from "lucide-react";

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
import { useCurrencyStore, type Currency } from "@/stores/currencyStore";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

// Menu items.
const items = [
    {
        title: "Dashboard",
        url: "/",
        icon: LayoutDashboard,
    },
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

const currencies: Currency[] = ['USD', 'EUR', 'GBP', 'CZK'];

export function AppSidebar() {
    const { selectedCurrency, setSelectedCurrency } = useCurrencyStore();

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

                <SidebarGroup>
                        <SidebarGroupLabel>Display Currency</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <div className="px-2 py-1">
                            <Select value={selectedCurrency} onValueChange={setSelectedCurrency}>
                                <SelectTrigger className="w-full">
                                    <DollarSign className="mr-2 h-4 w-4" />
                                    <SelectValue placeholder="Select currency" />
                                </SelectTrigger>
                                <SelectContent position="popper" side="right" align="start" sideOffset={5} className="z-50">
                                    {currencies.map((currency) => (
                                        <SelectItem key={currency} value={currency}>
                                            {currency}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
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
