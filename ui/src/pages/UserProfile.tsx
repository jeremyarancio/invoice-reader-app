import { useFetchUser } from "@/hooks/api/users";

function UserProfile() {
    const { user, isLoading } = useFetchUser();

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <p className="text-gray-500">Loading...</p>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="flex justify-center items-center h-screen">
                <p className="text-gray-500">
                    Error fetching your information...
                </p>
            </div>
        );
    }

    return (
        <>
            <div className="my-12 ml-15">
                <h1>Hey !👋 </h1>
            </div>
            <div className="ml-15 md:ml-30 flex gap-4">
                <p>{user.email}</p>
                {/* <Pen
                    onClick={onEdit}
                    className="size-5 text-gray-400 hover:text-gray-600 hover:cursor-pointer"
                /> */}
            </div>
        </>
    );
}

export default UserProfile;
