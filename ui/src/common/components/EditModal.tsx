import { useState } from "react";
import { Modal, Form, Button } from "react-bootstrap";

interface EditModalProps<T extends object> {
    item: T;
    disabled: string[];
    onClose: () => void;
    onUpdateItem: (item: T) => void;
    onDeleteItem: () => void;
}

function EditModal<T extends object>({
    item,
    disabled,
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
            onDeleteItem();
        }
    };

    return (
        <Modal show onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Form</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <Form onSubmit={handleEditSubmit}>
                    {Object.entries(item).map(([name, value]) => (
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
