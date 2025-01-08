import { Dropdown, Table, Button, Form } from "react-bootstrap";
import { useState } from "react";
import EditModal from "./EditModal";

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
    disabled: string[];
    onAddItem: () => void;
    onUpdateItem: (item: T) => void;
    onDeleteItems: (ids: T["id"][]) => void;
}

function TableRender<T extends BaseItem>({
    name,
    items,
    columns,
    disabled,
    onAddItem,
    onUpdateItem,
    onDeleteItems,
}: TableRenderProps<T>) {
    const [showedItem, setShowedItem] = useState<T | null>(null);
    const [selectedItems, setSelectedItems] = useState<T[]>([]);

    const handleSelect = (item: T) => {
        setSelectedItems((prev) => {
            if (prev.some((elt) => elt.id === item.id)) {
                return prev.filter((elt) => elt.id !== item.id);
            }
            return [...prev, item];
        });
    };

    const handleSelectAll = () => {
        const allCurrentPageItems = items.map((item) => item);
        const areAllSelected = allCurrentPageItems.every((item) =>
            selectedItems.some((selected) => selected.id === item.id)
        );

        if (areAllSelected) {
            setSelectedItems((prev) =>
                prev.filter(
                    (selected) =>
                        !allCurrentPageItems.some(
                            (item) => item.id === selected.id
                        )
                )
            );
        } else {
            setSelectedItems((prev) => {
                const newSelected = [...prev];
                allCurrentPageItems.forEach((item) => {
                    if (
                        !newSelected.some((selected) => selected.id === item.id)
                    ) {
                        newSelected.push(item);
                    }
                });
                return newSelected;
            });
        }
    };

    const isItemSelected = (item: T) => {
        return items.some((selected) => selected.id === item.id);
    };

    const renderCell = (item: T, column: ColumnConfig<T>) => {
        if (column.render) {
            return column.render(item);
        }
        const value = item[column.key as keyof T];
        return String(value ?? "");
    };

    const deleteItem = (id: T["id"]) => onDeleteItems([id]);

    return (
        <>
            {showedItem && (
                <EditModal<T>
                    item={showedItem}
                    disabled={disabled}
                    onClose={() => setShowedItem(null)}
                    onUpdateItem={onUpdateItem}
                    onDeleteItem={() => deleteItem(showedItem.id)}
                />
            )}
            <h2>{name}</h2>
            {selectedItems && (
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
                                onClick={() =>
                                    onDeleteItems(
                                        selectedItems.map((item) => item.id)
                                    )
                                }
                            >
                                <img src="src/assets/trash.svg"></img> Delete
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
                        {selectedItems && <th>Actions</th>}
                    </tr>
                </thead>
                <tbody>
                    {items.map((item) => (
                        <tr key={item.id}>
                            <td>
                                <Form.Check
                                    type="checkbox"
                                    onChange={() => handleSelect(item)}
                                    checked={isItemSelected(item)}
                                />
                            </td>
                            {columns.map((column) => (
                                <td key={`${item.id}-${String(column.key)}`}>
                                    {renderCell(item, column)}
                                </td>
                            ))}
                            <td>
                                <img
                                    src="src/assets/eye-fill.svg"
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
