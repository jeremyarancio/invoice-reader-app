interface BaseItem {
    id: string;
    name: string;
}

export interface FormGroup<T> {
    header: string;
    key: keyof T | string;
    formType:
        | "text"
        | "number"
        | "select"
        | "email"
        | "date"
        | "checkbox"
        | "password";
    required?: boolean;
    render?: (item: T) => string;
    fetchedItems?: BaseItem[];
    createItem?: () => void;
}
