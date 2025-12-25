import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { EllipsisVertical, Pencil, Trash2 } from "lucide-react";

interface Props {
    onEdit?: () => void;
    onDelete?: () => void;
}
function CardToggle({ onEdit, onDelete }: Props) {
    return (
        <>
            <Popover>
                <PopoverTrigger asChild>
                    <button>
                        <EllipsisVertical className="size-6 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 cursor-pointer" />
                    </button>
                </PopoverTrigger>
                <PopoverContent className="card-toggle-popover" align="start">
                    <div className="font-base space-y-2 grid grid-cols-1 ">
                        <button onClick={onEdit} className="card-toggle-button">
                            <Pencil />
                            <p>Edit</p>
                        </button>
                        <button onClick={onDelete} className="card-toggle-button">
                            <Trash2 />
                            <p>Delete</p>
                        </button>
                    </div>
                </PopoverContent>
            </Popover>
            <Popover></Popover>
        </>
    );
}

export default CardToggle;
