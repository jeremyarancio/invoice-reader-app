import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button"; // Assuming you're using shadcn/ui

export default function PageNotFound() {
    const navigate = useNavigate();

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4 text-center">
            <div className="max-w-md space-y-6">
                {/* Error graphic */}
                <div className="text-8xl font-bold text-gray-300">404</div>

                {/* Message */}
                <h1 className="text-3xl font-bold text-gray-900">
                    Page Not Found
                </h1>
                <p className="text-lg text-gray-600">
                    Oops! The page you're looking for doesn't exist or has been
                    moved.
                </p>

                {/* Action buttons */}
                <div className="flex gap-4 justify-center pt-4">
                    <Button
                        onClick={() => navigate(-1)}
                        variant="outline"
                        className="hover:cursor-pointer"
                    >
                        ← Go Back
                    </Button>
                    <Button
                        onClick={() => navigate("/invoices")}
                        className="hover:cursor-pointer"
                    >
                        Go Home
                    </Button>
                </div>
            </div>
        </div>
    );
}
