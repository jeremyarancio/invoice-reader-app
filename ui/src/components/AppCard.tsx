import type { ReactNode } from "react";
import CardToggle from "./CardToggle";

interface Props {
    children: ReactNode;
    onClick?: () => void;
    onEdit?: () => void;
    onDelete?: () => void;
}
export function AppCard({ children, onClick, onEdit, onDelete }: Props) {
    return (
        <div className="app-card">
            <div onClick={onClick} className="flex-col space-y-8 w-29/30">
                {children}
            </div>
            <div className="my-auto ml-auto w-1/30">
                <CardToggle onEdit={onEdit} onDelete={onDelete} />
            </div>
        </div>
    );
}
