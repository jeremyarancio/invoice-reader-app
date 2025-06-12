import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import {
    useFetchCurrencies,
    useFetchInvoice,
    useFetchInvoiceUrl,
} from "@/hooks/api/invoice";
import { useNavigate, useParams } from "react-router-dom";
import { useFetchClient } from "@/hooks/api/client";
import { z } from "zod";
import PdfPreview from "@/components/PdfPreview";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { CalendarIcon, Pencil, Save, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { useForm } from "react-hook-form";

function ViewInvoice() {
    const { invoiceId } = useParams();
    const [editMode, setEditMode] = useState(false);
    const navigate = useNavigate();

    const { invoice, isLoading: invoiceLoading } = useFetchInvoice(invoiceId);
    const { url: invoiceUrl } = useFetchInvoiceUrl(invoiceId);
    const { currencies } = useFetchCurrencies();
    const { client } = useFetchClient(invoice?.clientId);

    const invoiceSchema = z.object({
        invoiceNumber: z.string(),
        invoiceDescription: z.string(),
        grossAmount: z.coerce.number().min(0, "Must be positive"),
        currency: z.string(),
        vat: z.coerce.number().min(0).max(50),
        clientName: z.string(),
        issuedDate: z.date(),
        paidDate: z.date().optional(),
    });

    const form = useForm<z.infer<typeof invoiceSchema>>({
        resolver: zodResolver(invoiceSchema),
    });

    useEffect(() => {
        if (invoice) {
            form.setValue("invoiceNumber", invoice.invoiceNumber || "");
            form.setValue("invoiceDescription", "");
            form.setValue("grossAmount", invoice.grossAmount || 0);
            form.setValue(
                "currency",
                currencies?.find((c) => c.id === invoice?.currencyId)?.name ||
                    ""
            );
            form.setValue("vat", invoice.vat || 0);
            form.setValue("clientName", client?.clientName || "");
            form.setValue(
                "issuedDate",
                invoice.issuedDate ? new Date(invoice.issuedDate) : new Date()
            );
            form.setValue("paidDate", new Date());
        }
    }, [invoice, form]);

    const handleCancelEdit = () => {
        if (invoice) {
            form.reset({
                invoiceNumber: invoice.invoiceNumber || "",
                invoiceDescription: "",
                grossAmount: invoice.grossAmount || 0,
                currency:
                    currencies?.find((c) => c.id === invoice?.currencyId)
                        ?.name || "",
                vat: invoice.vat || 0,
                clientName: client?.clientName || "",
                issuedDate: invoice.issuedDate
                    ? new Date(invoice.issuedDate)
                    : new Date(),
                paidDate: new Date(),
            });
            setEditMode(false);
        }
    };

    const onSubmit = (values: z.infer<typeof invoiceSchema>) => {};

    return (
        <>
            <div className="flex mt-20 mb-40 justify-around">
                {invoiceUrl && (
                    <div className="px-4 flex justify-center">
                        <PdfPreview file={invoiceUrl} />
                    </div>
                )}
                <div className="px-4 md:px-20 w-full">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-2xl font-bold">
                            {invoiceId ? "Invoice Details" : "New Invoice"}
                        </h1>
                        <div className="flex gap-2">
                            <Button
                                variant="outline"
                                onClick={() => navigate("/invoices")}
                            >
                                Back to Invoices
                            </Button>
                            {editMode ? (
                                <>
                                    <Button
                                        variant="outline"
                                        onClick={handleCancelEdit}
                                        className="flex items-center gap-2"
                                    >
                                        <X className="w-4 h-4" />
                                        <span>Cancel</span>
                                    </Button>
                                    <Button
                                        variant="default"
                                        onClick={form.handleSubmit(onSubmit)}
                                        className="flex items-center gap-2"
                                        disabled={form.formState.isSubmitting}
                                    >
                                        <Save className="w-4 h-4" />
                                        <span>
                                            {form.formState.isSubmitting
                                                ? "Saving..."
                                                : "Save"}
                                        </span>
                                    </Button>
                                </>
                            ) : (
                                <Button
                                    variant="outline"
                                    onClick={() => setEditMode(true)}
                                    className="flex items-center gap-2"
                                >
                                    <Pencil className="w-4 h-4" />
                                    <span>Edit</span>
                                </Button>
                            )}
                        </div>
                    </div>

                    <Form {...form}>
                        <form
                            onSubmit={form.handleSubmit(onSubmit)}
                            className="space-y-6"
                        >
                            <FormField
                                control={form.control}
                                name="invoiceNumber"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Invoice Number</FormLabel>
                                        <FormControl>
                                            <Input
                                                {...field}
                                                readOnly={!editMode}
                                                className={
                                                    !editMode ? "bg-muted" : ""
                                                }
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="invoiceDescription"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Description</FormLabel>
                                        <FormControl>
                                            <Input
                                                {...field}
                                                readOnly={!editMode}
                                                className={
                                                    !editMode ? "bg-muted" : ""
                                                }
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="grossAmount"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Amount</FormLabel>
                                        <FormControl>
                                            <Input
                                                type="number"
                                                {...field}
                                                readOnly={!editMode}
                                                className={
                                                    !editMode ? "bg-muted" : ""
                                                }
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="currency"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Currency</FormLabel>
                                        {editMode ? (
                                            <Select
                                                onValueChange={field.onChange}
                                                value={field.value}
                                            >
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select currency" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    {currencies.map(
                                                        (currency) => (
                                                            <SelectItem
                                                                key={
                                                                    currency.id
                                                                }
                                                                value={
                                                                    currency.id
                                                                }
                                                            >
                                                                {currency.name}
                                                            </SelectItem>
                                                        )
                                                    )}
                                                </SelectContent>
                                            </Select>
                                        ) : (
                                            <Input
                                                value={field.value}
                                                readOnly
                                                className="bg-muted"
                                            />
                                        )}
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="issuedDate"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Issued Date</FormLabel>
                                        {editMode ? (
                                            <Popover>
                                                <PopoverTrigger asChild>
                                                    <FormControl>
                                                        <Button
                                                            variant={"outline"}
                                                            className={cn(
                                                                "w-full pl-3 text-left font-normal",
                                                                !field.value &&
                                                                    "text-muted-foreground"
                                                            )}
                                                        >
                                                            {field.value ? (
                                                                field.value.toLocaleDateString()
                                                            ) : (
                                                                <span>
                                                                    Pick a date
                                                                </span>
                                                            )}
                                                            <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                                        </Button>
                                                    </FormControl>
                                                </PopoverTrigger>
                                                <PopoverContent
                                                    className="w-auto p-0"
                                                    align="start"
                                                >
                                                    <Calendar
                                                        mode="single"
                                                        selected={field.value}
                                                        onSelect={
                                                            field.onChange
                                                        }
                                                        initialFocus
                                                    />
                                                </PopoverContent>
                                            </Popover>
                                        ) : (
                                            <Input
                                                value={
                                                    field.value
                                                        ? field.value.toLocaleDateString()
                                                        : ""
                                                }
                                                readOnly
                                                className="bg-muted"
                                            />
                                        )}
                                    </FormItem>
                                )}
                            />

                            {editMode && (
                                <Button type="submit" className="w-full">
                                    Edit
                                </Button>
                            )}
                        </form>
                    </Form>
                </div>
            </div>
        </>
    );
}

export default ViewInvoice;
