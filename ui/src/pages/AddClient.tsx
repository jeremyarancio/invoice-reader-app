import { ArrowLeft } from "lucide-react";
import { useState } from "react";
import AppAlert from "@/components/AppAlert";
import { useNavigate } from "react-router-dom";
import AddCompany from "@/components/addClient/AddCompany";
import AddIndividual from "@/components/addClient/AddIndividual";
import { useIsSubmittedAlert } from "@/hooks/alert-hooks";

function AddClient() {
    const [clientType, setClientType] = useState<string>("company");
    const navigate = useNavigate();
    const { isSubmitted } = useIsSubmittedAlert();

    const onSuccess = () => {
        navigate("/clients");
    };

    return (
        <>
            <div className="mt-10 ml-10">
                <button
                    onClick={() => navigate("/clients")}
                    className="hover:cursor-pointer"
                >
                    <ArrowLeft
                        size={40}
                        className="rounded-full hover:bg-stone-50"
                    />
                </button>
            </div>
            <p className="my-15 ml-30 md:ml-60 font-semibold">My client is</p>
            <div className="flex justify-center items-center space-x-6 mb-15">
                <button
                    onClick={() => setClientType("company")}
                    className={`button-primary ${
                        clientType === "company"
                            ? "bg-stone-600 text-gray-100"
                            : ""
                    }`}
                >
                    A company
                </button>
                <button
                    onClick={() => setClientType("individual")}
                    className={`button-primary ${
                        clientType === "individual"
                            ? "bg-stone-600 text-gray-100"
                            : ""
                    }`}
                >
                    An individual
                </button>
            </div>
            <div className="max-w-md mx-auto mb-30">
                {clientType === "company" ? (
                    <AddCompany onSuccess={onSuccess} />
                ) : (
                    <AddIndividual />
                )}
            </div>
            {isSubmitted && <AppAlert />}
        </>
    );
}

export default AddClient;
