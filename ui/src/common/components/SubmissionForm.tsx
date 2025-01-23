import React, { useState } from "react";
import { Alert, Form, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { FormGroup } from "@/common/types";

interface BaseItem {
    id: string;
    name: string;
}

interface Props<T> {
    name?: string;
    formGroups: FormGroup<T>[];
    submit: (item: T) => void;
    additionalItems?: BaseItem[]; // It can take more attributes
    initialData: T;
}

function SubmissionForm<T>({
    name,
    formGroups,
    submit,
    additionalItems,
    initialData,
}: Props<T>) {
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState<T>(initialData);
    const navigate = useNavigate();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const missingRequired = formGroups
            .filter((formGroup) => formGroup.required)
            .some((formGroup) => !formData[formGroup.key as keyof T]);

        if (missingRequired) {
            setError("Please fill in all required fields");
            return;
        }
        submit(formData as T);
        navigate("/");
    };

    const handleInputChange = (key: string, value: any) => {
        setFormData((prev) => ({
            ...prev,
            [key]: value,
        }));
    };

    const renderCell = (item: T, formGroup: FormGroup<T>) => {
        if (formGroup.render) {
            return formGroup.render(item);
        }
        return String(item[formGroup.key as keyof T] ?? "");
    };

    return (
        <>
            {error && (
                <Alert
                    variant="danger"
                    onClose={() => setError(null)}
                    dismissible
                    className="mb-4"
                >
                    {error}
                </Alert>
            )}

            <Form onSubmit={handleSubmit}>
                {name && <h3 className="mb-4">{name}</h3>}
                {formGroups.map((formGroup) => (
                    <Form.Group className="mb-3" key={String(formGroup.key)}>
                        <Form.Label>
                            {formGroup.header}
                            {formGroup.required && (
                                <span className="text-danger">*</span>
                            )}
                        </Form.Label>

                        {formGroup.formType === "select" ? (
                            <Form.Select
                                onChange={(e) =>
                                    handleInputChange(
                                        String(formGroup.key),
                                        e.target.value
                                    )
                                }
                                required={formGroup.required}
                                value={String(
                                    formData[formGroup.key as keyof T] || ""
                                )}
                            >
                                <option value="">Select an item</option>
                                {additionalItems?.map((item) => (
                                    <option key={item.id} value={item.id}>
                                        {item.name}
                                    </option>
                                ))}
                            </Form.Select>
                        ) : formGroup.formType === "checkbox" ? (
                            <Form.Check
                                type="checkbox"
                                onChange={(e) =>
                                    handleInputChange(
                                        String(formGroup.key),
                                        e.target.checked
                                    )
                                }
                                name={String(formGroup.key)}
                            />
                        ) : (
                            <Form.Control
                                type={formGroup.formType}
                                name={String(formGroup.key)}
                                onChange={(e) =>
                                    handleInputChange(
                                        String(formGroup.key),
                                        e.target.value
                                    )
                                }
                                required={formGroup.required}
                                value={renderCell(formData, formGroup)}
                            />
                        )}
                    </Form.Group>
                ))}
                <div className="text-center mt-4">
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </div>
            </Form>
        </>
    );
}

export default SubmissionForm;
