import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { Modal, Form, Button } from "react-bootstrap";

interface EditModalProps<T extends object> {
    entity: T;
    disabled: string[];
    onClose: () => void;
    updateFn: (entity: T) => Promise<any>;
    deleteFn: (entity: T) => Promise<any>;
}

function EditModal<T extends object>({
    entity,
    disabled,
    onClose,
    updateFn,
    deleteFn,
}: EditModalProps<T>) {
    const [formData, setFormData] = useState<T>(entity);
    const [isEditToSubmit, setIsEditToSubmit] = useState(false);

    const updateMutation = useMutation({
        mutationFn: updateFn,
        onSuccess: () => {
            window.alert("Successfully updated.");
            onClose();
        },
        onError: (err) => {
            const errorMessage =
                err instanceof Error
                    ? err.message
                    : "An unexpected error occurred";
            window.alert("Error: " + errorMessage);
        },
    });

    const deleteMutation = useMutation({
        mutationFn: deleteFn,
        onSuccess: () => {
            window.alert("Successfully deleted");
            onClose();
        },
        onError: (error: Error) => {
            window.alert("Failed to delete: " + error.message);
        },
    });

    const handleClose = () => {
        setIsEditToSubmit(false);
        onClose();
    };

    const handleChange = (name: string, value: any) => {
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleEditSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        updateMutation.mutate(formData);
    };

    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this item?")) {
            deleteMutation.mutate(entity);
        }
    };

    return (
        <Modal show onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Form</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <Form onSubmit={handleEditSubmit}>
                    {Object.entries(entity).map(([name, value]) => (
                        <Form.Group className="mb-3" key={name}>
                            <Form.Label>{name}</Form.Label>
                            <Form.Control
                                type="text"
                                name={name}
                                placeholder={String(value)}
                                value={formData[name as keyof T] as string}
                                onChange={(e) =>
                                    handleChange(name, e.target.value)
                                }
                                disabled={
                                    !isEditToSubmit || disabled.includes(name)
                                }
                            />
                        </Form.Group>
                    ))}
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                {!isEditToSubmit && (
                    <Button variant="outline-danger" onClick={handleDelete}>
                        Delete
                    </Button>
                )}
                <Button
                    variant={isEditToSubmit ? "warning" : "primary"}
                    onClick={
                        isEditToSubmit
                            ? handleEditSubmit
                            : () => setIsEditToSubmit(true)
                    }
                    type={isEditToSubmit ? "submit" : "button"}
                >
                    {isEditToSubmit ? "Save Changes" : "Edit"}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default EditModal;
