import { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const UploadInvoice = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(e)
    if (file) {
      alert(`Uploaded file: ${file.name}`);
    }
  };

  return (
    <div>
      <h2>Upload Invoice</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Select Invoice PDF</Form.Label>
          <Form.Control type="file" accept="application/pdf" onChange={handleFileChange} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Upload
        </Button>
      </Form>
    </div>
  );
};

export default UploadInvoice;
