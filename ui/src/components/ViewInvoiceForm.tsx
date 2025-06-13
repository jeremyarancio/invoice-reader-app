import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { CalendarIcon, Pencil, Save, X } from "lucide-react";
import { useUpdateInvoice } from "@/hooks/api/invoice";
import type { Currency, Invoice } from "@/schemas/invoice";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Calendar } from "@/components/ui/calendar";
import type { Client } from "@/schemas/client";

interface Props {
    invoice: Invoice;
    currencies: Currency[];
    clients: Client[];
}

function ViewInvoiceForm({ invoice, clients, currencies }: Props) {
    const [editMode, setEditMode] = useState(false);

    const updateInvoice = useUpdateInvoice();

    const invoiceSchema = z.object({
        invoiceNumber: z.string(),
        invoiceDescription: z.string(),
        grossAmount: z.coerce.number().min(0, "Must be positive"),
        currencyId: z.string(),
        vat: z.coerce.number().min(0).max(50),
        clientId: z.string(),
        issuedDate: z.date(),
        paidDate: z.date().optional(),
    });

    const form = useForm<z.infer<typeof invoiceSchema>>({
        resolver: zodResolver(invoiceSchema),
        defaultValues: {
            invoiceNumber: invoice.invoiceNumber,
            invoiceDescription: "",
            grossAmount: invoice.grossAmount,
            currencyId: invoice.currencyId,
            vat: invoice.vat,
            clientId: invoice.clientId,
            issuedDate: new Date(invoice.issuedDate),
            paidDate: undefined,
        },
    });

    const handleCancelEdit = () => {
        form.reset({
            invoiceNumber: invoice.invoiceNumber,
            invoiceDescription: "",
            grossAmount: invoice.grossAmount,
            currencyId: invoice.currencyId,
            vat: invoice.vat,
            clientId: invoice.clientId,
            issuedDate: new Date(invoice.issuedDate),
            paidDate: undefined,
        });
        setEditMode(false);
    };

    const onSubmit = (values: z.infer<typeof invoiceSchema>) => {
        updateInvoice({
            id: invoice.id,
            invoiceNumber: values.invoiceNumber,
            grossAmount: values.grossAmount,
            currencyId: values.currencyId,
            vat: values.vat,
            clientId: values.clientId,
            issuedDate: values.issuedDate,
            status: !!values.paidDate,
        });
        setEditMode(false);
    };

    return (
        <>
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
                                        className={!editMode ? "bg-muted" : ""}
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
                                        className={!editMode ? "bg-muted" : ""}
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
                                        className={!editMode ? "bg-muted" : ""}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="currencyId"
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

                                        <SelectContent className="bg-stone-50">
                                            {currencies.map((currency) => (
                                                <SelectItem
                                                    key={currency.id}
                                                    value={currency.id}
                                                >
                                                    {currency.name}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                ) : (
                                    <Input
                                        value={
                                            currencies.find(
                                                (c) => c.id === field.value
                                            )?.name || ""
                                        }
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
                        name="clientId"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Client
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                {editMode ? (
                                    <div className="flex gap-2 items-center">
                                        <Select
                                            onValueChange={field.onChange}
                                            value={field.value}
                                        >
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select a Client" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent className="bg-stone-50">
                                                {clients.map((client) => (
                                                    <SelectItem
                                                        key={client.id}
                                                        value={client.id}
                                                    >
                                                        {client.clientName}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                ) : (
                                    <Input
                                        value={
                                            clients.find(
                                                (c) => c.id === field.value
                                            )?.clientName || ""
                                        }
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
                                                        <span>Pick a date</span>
                                                    )}
                                                    <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                                </Button>
                                            </FormControl>
                                        </PopoverTrigger>
                                        <PopoverContent
                                            className="w-auto p-0 bg-stone-50"
                                            align="start"
                                        >
                                            <Calendar
                                                mode="single"
                                                selected={field.value}
                                                onSelect={field.onChange}
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
                </form>
            </Form>
            <div className="flex justify-end items-center mt-6">
                <div className="flex gap-2">
                    {editMode ? (
                        <>
                            <button
                                className="flex items-center gap-2 button-secondary bg-red-50"
                                onClick={handleCancelEdit}
                            >
                                <X className="w-4 h-4" />
                                <span>Cancel</span>
                            </button>
                            <button
                                onClick={form.handleSubmit(onSubmit)}
                                className="flex items-center gap-2 button-secondary"
                                disabled={form.formState.isSubmitting}
                            >
                                <Save className="w-4 h-4" />
                                <span>
                                    {form.formState.isSubmitting
                                        ? "Saving..."
                                        : "Save"}
                                </span>
                            </button>
                        </>
                    ) : (
                        <button
                            onClick={() => setEditMode(true)}
                            className="flex items-center gap-2 button-secondary"
                        >
                            <Pencil className="w-4 h-4" />
                            <span>Edit</span>
                        </button>
                    )}
                </div>
            </div>
        </>
    );
}

export default ViewInvoiceForm;
