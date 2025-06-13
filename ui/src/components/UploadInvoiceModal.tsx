// components/UploadInvoiceModal.tsx
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type React from "react";
import { useState } from "react";

interface Props {
    trigger: React.ReactNode;
    handleUpload: () => void;
    setSelectedFile: React.Dispatch<any>;
}

const UploadInvoiceModal = ({
    trigger,
    handleUpload,
    setSelectedFile,
}: Props) => {
    const [showErrorMessage, setShowErrorMessage] = useState<
        boolean | undefined
    >(undefined);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setSelectedFile(e.target.files[0]);
            setShowErrorMessage(false);
        }
    };

    const handleUploadClick = () => {
        showErrorMessage === undefined
            ? setShowErrorMessage(true)
            : !showErrorMessage && handleUpload();
    };

    return (
        <Dialog>
            <DialogTrigger asChild>{trigger}</DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle className="text-2xl">
                        Upload your invoice
                    </DialogTitle>
                    <DialogDescription>
                        Upload your invoice file here.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="invoice-file" className="text-right">
                            File
                        </Label>
                        <div className="col-span-3 ">
                            <Input
                                id="invoice-file"
                                type="file"
                                onChange={handleChange}
                            />
                            {showErrorMessage === true && (
                                <p className="text-red-500 text-sm">
                                    You need to upload a file.
                                </p>
                            )}
                        </div>
                    </div>
                </div>
                <DialogFooter>
                    <DialogClose
                        asChild
                        onClick={() => setShowErrorMessage(undefined)}
                    >
                        <Button variant="outline">Cancel</Button>
                    </DialogClose>
                    <Button type="submit" onClick={handleUploadClick}>
                        Upload
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default UploadInvoiceModal;
