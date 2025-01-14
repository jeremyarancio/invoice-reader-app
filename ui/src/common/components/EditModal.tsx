import React, { useState } from "react";
import { Modal, Form, Button } from "react-bootstrap";

interface BaseItem {
    id: string;
}

interface EditField<T> {
    header: string;
    key: keyof T | string;
    render?: () => React.ReactNode;
}

interface EditModalProps<T extends BaseItem> {
    item: T;
    disabledFields?: string[];
    editFields: EditField<T>[];
    onClose: () => void;
    onUpdateItem: (item: T) => void;
    onDeleteItem: (id: T) => void;
}

function EditModal<T extends BaseItem>({
    item,
    disabledFields,
    editFields,
    onClose,
    onUpdateItem,
    onDeleteItem,
}: EditModalProps<T>) {
    const [formData, setFormData] = useState<T>(item);
    const [isEditToSubmit, setIsEditToSubmit] = useState(false);

    const handleClose = () => {
        setIsEditToSubmit(false);
        onClose();
    };

    const handleChange = (name: string, value: any) => {
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleEditSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onUpdateItem(formData);
    };

    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this item?")) {
            onDeleteItem(item);
        }
    };

    return (
        <Modal show onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Form</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <Form onSubmit={handleEditSubmit}>
                    {editFields.map((field) => (
                        <Form.Group className="mb-3" key={String(field.key)}>
                            <Form.Label>{field.header}</Form.Label>
                            <Form.Control
                                type="text"
                                name={field.header}
                                placeholder={String(
                                    formData[field.key as keyof T]
                                )}
                                value={formData[field.key as keyof T] as string}
                                onChange={(e) =>
                                    handleChange(
                                        String(field.key),
                                        e.target.value
                                    )
                                }
                                disabled={
                                    !isEditToSubmit ||
                                    disabledFields?.includes(
                                        String(field.key)
                                    ) ||
                                    false
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
