import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import AddCompany from "./addClient/AddCompany";
import { useState } from "react";
import AddIndividual from "./addClient/AddIndividual";
import { useNewClientModalStore } from "@/stores/new-client-modal-store";

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

function NewClientModal({ isOpen, onClose }: Props) {
    const [clientType, setClientType] = useState("company");
    const { closeNewClientModal } = useNewClientModalStore();

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-lg max-h-150 overflow-y-auto p-15">
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
                {clientType === "company" && (
                    <AddCompany onSuccess={closeNewClientModal} />
                )}
                {clientType === "individual" && (
                    <AddIndividual /> //NOt implemented yet
                )}
            </DialogContent>
        </Dialog>
    );
}

export default NewClientModal;
