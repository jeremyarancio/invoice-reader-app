import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, FileText, Users, List } from "lucide-react";
import { useNavigate } from "react-router-dom";
import UploadInvoiceModal from "@/components/UploadInvoiceModal";
import { useState } from "react";

export function QuickActionsSection() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleUpload = () => {
    if (selectedFile) {
      navigate("/invoices/add", { state: { file: selectedFile } });
    }
  };

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <UploadInvoiceModal
            trigger={
              <Button className="w-full" size="lg">
                <Plus className="mr-2 h-4 w-4" />
                Add Invoice
              </Button>
            }
            handleUpload={handleUpload}
            setSelectedFile={setSelectedFile}
          />

          <Button
            variant="outline"
            className="w-full"
            size="lg"
            onClick={() => navigate("/clients/add")}
          >
            <Users className="mr-2 h-4 w-4" />
            Add Client
          </Button>

          <Button
            variant="outline"
            className="w-full"
            size="lg"
            onClick={() => navigate("/invoices")}
          >
            <FileText className="mr-2 h-4 w-4" />
            View Invoices
          </Button>

          <Button
            variant="outline"
            className="w-full"
            size="lg"
            onClick={() => navigate("/clients")}
          >
            <List className="mr-2 h-4 w-4" />
            View Clients
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
