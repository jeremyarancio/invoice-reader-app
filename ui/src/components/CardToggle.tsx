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
                        <EllipsisVertical className="size-6 text-gray-500 hover:text-gray-700 cursor-pointer" />
                    </button>
                </PopoverTrigger>
                <PopoverContent className="bg-stone-50 w-30" align="start">
                    <div className="font-base space-y-2 grid grid-cols-1 ">
                        <button onClick={onEdit} className="flex items-center space-x-2 w-full hover:bg-stone-100 hover:cursor-pointer">
                            <Pencil />
                            <p>Edit</p>
                        </button>
                        <button onClick={onDelete} className="flex items-center space-x-2 hover:bg-stone-100 hover:cursor-pointer">
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
