import { Alert } from "react-bootstrap";

function AlertError({ error, onClose }: { error: Error; onClose: () => void }) {
    return (
        <Alert variant="danger" onClose={onClose} dismissible className="mb-4">
            {error.message}
        </Alert>
    );
}

export default AlertError;
