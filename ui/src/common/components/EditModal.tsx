import React, { useState } from "react";
import { Modal, Form, Button, Container, Col, Row } from "react-bootstrap";
import PdfPreview from "@/common/components/PdfPreview";

interface BaseItem {
    id: string;
}

interface EditField<T> {
    header: string;
    key: keyof T | string;
    render?: (item: T) => React.ReactNode;
}

interface EditModalProps<T extends BaseItem> {
    item: T;
    disabledFields?: string[];
    editFields: EditField<T>[];
    filePreview?: File | string | null;
    onClose: () => void;
    onUpdateItem: (item: T) => void;
    onDeleteItem: (id: T) => void;
}

function EditModal<T extends BaseItem>({
    item,
    disabledFields,
    editFields,
    filePreview,
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

    const handleChange = (key: string, value: any) => {
        setFormData((prev) => ({ ...prev, [key]: value }));
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
        <Modal show onHide={handleClose} size="xl">
            <Modal.Header closeButton>
                <Modal.Title>Form</Modal.Title>
            </Modal.Header>
            <Container>
                <Row>
                    {filePreview && (
                        <Col>
                            <PdfPreview file={filePreview} />
                        </Col>
                    )}
                    <Col>
                        <Modal.Body>
                            <Form onSubmit={handleEditSubmit}>
                                {editFields.map((field) => (
                                    <Form.Group
                                        className="mb-3"
                                        key={String(field.key)}
                                    >
                                        <Form.Label>{field.header}</Form.Label>
                                        {typeof formData[
                                            field.key as keyof T
                                        ] === "boolean" ? (
                                            <Form.Check
                                                type="checkbox"
                                                name={field.header}
                                                onChange={(e) =>
                                                    handleChange(
                                                        String(field.key),
                                                        e.target.checked
                                                    )
                                                }
                                                checked={
                                                    formData[
                                                        field.key as keyof T
                                                    ] as boolean
                                                }
                                                disabled={
                                                    !isEditToSubmit ||
                                                    disabledFields?.includes(
                                                        String(field.key)
                                                    ) ||
                                                    false
                                                }
                                            />
                                        ) : (
                                            <Form.Control
                                                type="text"
                                                name={field.header}
                                                placeholder={String(
                                                    formData[
                                                        field.key as keyof T
                                                    ]
                                                )}
                                                value={
                                                    formData[
                                                        field.key as keyof T
                                                    ] as string
                                                }
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
                                        )}
                                    </Form.Group>
                                ))}
                            </Form>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={handleClose}>
                                Close
                            </Button>
                            {!isEditToSubmit && (
                                <Button
                                    variant="outline-danger"
                                    onClick={handleDelete}
                                >
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
                    </Col>
                </Row>
            </Container>
        </Modal>
    );
}

export default EditModal;
