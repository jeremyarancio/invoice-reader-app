import { Dropdown, Table, Button, Form } from "react-bootstrap";
import { useState } from "react";
import { EditModal, EditField } from "./EditModal";
import trashIcon from "@/images/trash.svg";
import viewIcon from "@/images/eye-fill.svg";

interface BaseItem {
    id: string;
}

interface ColumnConfig<T> {
    header: string;
    key: keyof T | string;
    render?: (item: T) => React.ReactNode;
}

interface TableRenderProps<T extends BaseItem> {
    name: string;
    items: T[];
    columns: ColumnConfig<T>[];
    editFields: EditField<T>[];
    disabledFields?: string[];
    filePreviews?: { id: string; file?: File | string | null }[];
    onAddItem: () => void;
    onUpdateItem: (item: T) => void;
    onDeleteItems: (items: T[]) => void;
}

function TableRender<T extends BaseItem>({
    name,
    items,
    columns,
    editFields,
    disabledFields,
    filePreviews,
    onAddItem,
    onUpdateItem,
    onDeleteItems,
}: TableRenderProps<T>) {
    const [showedItem, setShowedItem] = useState<T | null>(null);
    const [selectedItems, setSelectedItems] = useState<T[]>([]);

    const handleSelect = (item: T) => {
        setSelectedItems((prev) => {
            if (prev.includes(item)) {
                return prev.filter((elt) => elt !== item);
            }
            return [...prev, item];
        });
    };

    const handleSelectAll = () => {
        const areAllSelected = items.every((item) =>
            selectedItems.includes(item)
        );

        if (areAllSelected) {
            setSelectedItems([]);
        } else {
            setSelectedItems(items);
        }
    };

    const renderCell = (item: T, column: ColumnConfig<T>) => {
        if (column.render) {
            return column.render(item);
        }
        const value = item[column.key as keyof T];
        return String(value ?? "");
    };

    const handleDeleteItem = (item: T) => onDeleteItems([item]);

    const getFilePreview = () => {
        const filePreview =
            showedItem &&
            filePreviews?.find(
                (filePreview) => filePreview.id === showedItem.id
            );
        return filePreview?.file;
    };

    return (
        <>
            {showedItem && (
                <EditModal<T>
                    item={showedItem}
                    editFields={editFields}
                    disabledFields={disabledFields}
                    onClose={() => setShowedItem(null)}
                    onUpdateItem={onUpdateItem}
                    onDeleteItem={handleDeleteItem}
                    filePreview={getFilePreview()}
                />
            )}
            <h2>{name}</h2>
            {selectedItems.length > 0 && (
                <div className="d-flex justify-content-end align-items-center">
                    <Dropdown>
                        <Dropdown.Toggle
                            variant="secondary"
                            id="dropdown-basic"
                        >
                            Actions
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item
                                href="#/delete"
                                onClick={() => onDeleteItems(selectedItems)}
                            >
                                <img src={trashIcon}></img> Delete
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
            )}

            <Table striped hover responsive>
                <thead>
                    <tr>
                        <th>
                            <Form.Check
                                type="checkbox"
                                onChange={handleSelectAll}
                                checked={selectedItems.length === items.length}
                            />
                        </th>
                        {columns.map((column) => (
                            <th key={String(column.key)}>{column.header}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {items.map((item) => (
                        <tr key={`row-${item.id}`}>
                            <td>
                                <Form.Check
                                    type="checkbox"
                                    onChange={() => handleSelect(item)}
                                    checked={selectedItems.includes(item)}
                                />
                            </td>
                            {columns.map((column) => (
                                <td key={`${item.id}-${String(column.key)}`}>
                                    {renderCell(item, column)}
                                </td>
                            ))}
                            <td>
                                <img
                                    src={viewIcon}
                                    alt="view"
                                    onClick={() => setShowedItem(item)}
                                    style={{ cursor: "pointer" }}
                                    className="me-2"
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <div className="text-muted">
                Total {name}: {items.length}
            </div>
            <div className="mb-3 d-flex justify-content-end align-items-center">
                <Button onClick={onAddItem} variant="primary">
                    Add {name}
                </Button>
            </div>
        </>
    );
}

export default TableRender;
