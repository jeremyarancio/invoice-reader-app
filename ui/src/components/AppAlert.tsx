import { Check, X } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";
import { useIsSubmittedAlert } from "@/hooks/alert-hooks";

function AppAlert() {
    const { setIsSubmitted } = useIsSubmittedAlert();

    return (
        <div className="flex sticky justify-end bottom-3 mr-10 transition duration-500">
            <Alert className="w-sm flex justify-start">
                <Check className="" />
                <div>
                    <AlertTitle>Heads up!</AlertTitle>
                    <AlertDescription>
                        Your invoice was succesfully added.
                    </AlertDescription>
                </div>
                <button
                    className="ml-auto"
                    onClick={() => setIsSubmitted(false)}
                >
                    <X />
                </button>
            </Alert>
        </div>
    );
}

export default AppAlert;
