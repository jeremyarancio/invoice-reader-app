import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import AddCompanyLayout from "./addClient/AddCompanyLayout";
import { useState } from "react";
import AddIndividualLayout from "./addClient/AddIndividualLayout";

interface NewClientModalProps {
    isOpen: boolean;
    onClose: () => void;
}

function NewClientModal({ isOpen, onClose }: NewClientModalProps) {
    const [clientType, setClientType] = useState("company");

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-lg max-h-150 overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Create New Client</DialogTitle>
                    <DialogDescription>
                        Add a new client to your system.
                    </DialogDescription>
                </DialogHeader>
                <div className="flex gap-4 justify-center my-6">
                    <button
                        onClick={() => setClientType("company")}
                        className={`button-secondary ${
                            clientType === "company"
                                ? "bg-stone-600 text-gray-100"
                                : ""
                        }`}
                    >
                        A company
                    </button>
                    <button
                        onClick={() => setClientType("individual")}
                        className={`button-secondary ${
                            clientType === "individual"
                                ? "bg-stone-600 text-gray-100"
                                : ""
                        }`}
                    >
                        An individual
                    </button>
                </div>
                {clientType === "company" && <AddCompanyLayout />}
                {clientType === "individual" && <AddIndividualLayout />}
            </DialogContent>
        </Dialog>
    );
}

export default NewClientModal;
