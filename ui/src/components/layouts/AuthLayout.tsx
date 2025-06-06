import { Outlet } from "react-router-dom";

export function AuthLayout() {
    return (
        <div className="grid grid-cols-6 h-screen">
            <div className="col-span-2 flex flex-col p-4 justify-center">
                <div className="w-full max-w-xs mx-auto space-y-8">
                    <div className="space-y-2">
                        <h1>Welcome!</h1>
                    </div>
                    <div className="space-y-6">
                        <Outlet />
                    </div>
                </div>
            </div>

            <div className="col-span-4 bg-gradient-to-br from-blue-50 to-gray-100 h-full flex items-center justify-center">
                <div className="max-w-lg p-8 text-center">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                        Streamline Your Workflow
                    </h2>
                    <p className="text-gray-600">
                        Our platform helps you manage projects efficiently with
                        powerful tools and integrations.
                    </p>
                </div>
            </div>
        </div>
    );
}
