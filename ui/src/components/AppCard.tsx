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
        <div className="flex justify-between w-full h-30 pl-6 pr-4 py-4 rounded-lg border-1 shadow-lg transition-all duration-200 ease-in-out transform hover:-translate-y-0.5 hover:cursor-pointer">
            <div onClick={onClick} className="flex-col space-y-8 w-29/30">
                {children}
            </div>
            <div className="my-auto ml-auto w-1/30">
                <CardToggle onEdit={onEdit} onDelete={onDelete} />
            </div>
        </div>
    );
}
