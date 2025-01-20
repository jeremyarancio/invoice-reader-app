import { Document, Page, pdfjs } from "react-pdf";
import { useState } from "react";
import { Button } from "react-bootstrap";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface PdfPreviewProps {
    file: File;
}

function PdfPreview({ file }: PdfPreviewProps) {
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [numPages, setNumPages] = useState<number>();

    const onDocumentLoadSucces = ({ numPages }: any) => {
        setNumPages(numPages);
    };

    const handlePrevPage = () => {
        setPageNumber(pageNumber - 1);
    };

    const handleNextPage = () => {
        setPageNumber(pageNumber + 1);
    };

    return (
        <div>
            <div className="d-flex justify-content-center align-items-center gap-3 mt-3">
                <Document file={file} onLoadSuccess={onDocumentLoadSucces}>
                    <Page
                        pageNumber={pageNumber}
                        renderTextLayer={false}
                        renderAnnotationLayer={false}
                    ></Page>
                </Document>
            </div>
            <div className="d-flex justify-content-center align-items-center gap-3 mt-3">
                <Button
                    onClick={handlePrevPage}
                    disabled={pageNumber <= 1}
                    variant="secondary"
                    size="sm"
                >
                    Previous
                </Button>
                <Button
                    onClick={handleNextPage}
                    disabled={pageNumber >= (numPages ?? -1)}
                    variant="secondary"
                    size="sm"
                >
                    Next
                </Button>
                <p className="mb-0">
                    Page {pageNumber} of {numPages}
                </p>
            </div>
        </div>
    );
}

export default PdfPreview;
