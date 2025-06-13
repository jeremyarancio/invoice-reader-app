import { user } from "@/types/user";
import { Pen } from "lucide-react";

function UserProfile() {
    const onEdit = () => {
        console.log("Edit");
    };
    return (
        <>
            <div className="my-12 ml-15">
                <h1>{user.username}</h1>
            </div>
            <div className="ml-15 md:ml-30 flex gap-4">
                <p>{user.email}</p>
                <Pen
                    onClick={onEdit}
                    className="size-5 text-gray-400 hover:text-gray-600 hover:cursor-pointer"
                />
            </div>
        </>
    );
}

export default UserProfile;
