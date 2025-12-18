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
import { CURRENCIES, type Invoice, type InvoiceData } from "@/schemas/invoice";
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
import { cn, toEuropeanDate } from "@/lib/utils";
import { Calendar } from "@/components/ui/calendar";
import type { Client } from "@/schemas/client";

interface Props {
    invoice: Invoice;
    clients: Client[];
}

function ViewInvoiceForm({ invoice, clients }: Props) {
    const [editMode, setEditMode] = useState(false);

    const updateInvoice = useUpdateInvoice();

    const invoiceSchema = z
        .object({
            invoiceNumber: z.string(),
            invoiceDescription: z.string(),
            grossAmount: z.coerce.number().min(0, "Must be positive"),
            currency: z.string(),
            vat: z.coerce.number().min(0).max(50),
            clientId: z.string(),
            issuedDate: z.date(),
            paidDate: z.date().optional(),
        })
        .refine((data) => !data.paidDate || data.paidDate >= data.issuedDate, {
            message: "Paid date cannot be before issued date",
            path: ["paidDate"],
        });

    const form = useForm<z.infer<typeof invoiceSchema>>({
        resolver: zodResolver(invoiceSchema),
        defaultValues: {
            invoiceNumber: invoice.invoiceNumber,
            invoiceDescription: invoice.description,
            grossAmount: invoice.grossAmount,
            currency: invoice.currency,
            vat: invoice.vat,
            clientId: invoice.clientId,
            issuedDate: new Date(invoice.issuedDate),
            paidDate: invoice.paidDate ? new Date(invoice.paidDate) : undefined,
        },
    });

    const cancelEdit = () => {
        form.reset({
            invoiceNumber: invoice.invoiceNumber,
            invoiceDescription: invoice.description,
            grossAmount: invoice.grossAmount,
            currency: invoice.currency,
            vat: invoice.vat,
            clientId: invoice.clientId,
            issuedDate: new Date(invoice.issuedDate),
            paidDate: undefined,
        });
        setEditMode(false);
    };

    const onSubmit = async (values: z.infer<typeof invoiceSchema>) => {
        // We use async to wait fot the mutation to complete
        // before setting edit mode to false.
        try {
            const invoiceData: InvoiceData = {
                invoiceNumber: values.invoiceNumber,
                grossAmount: values.grossAmount,
                currency: values.currency,
                vat: values.vat,
                issuedDate: values.issuedDate,
                paidDate: values.paidDate,
                description: values.invoiceDescription,
            };
            await updateInvoice(invoice.id, invoiceData, values.clientId);
            setEditMode(false);
        } catch (error) {
            cancelEdit();
        }
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
                    <div className="grid grid-cols-4 gap-4">
                        <FormField
                            control={form.control}
                            name="grossAmount"
                            render={({ field }) => (
                                <FormItem className="col-span-3">
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
                                <FormItem className="col-span-1">
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
                                                {Object.entries(CURRENCIES).map(
                                                    ([key, value]) => (
                                                        <SelectItem
                                                            key={key}
                                                            value={value.symbol}
                                                        >
                                                            {value.symbol} -{" "}
                                                            {value.name}
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
                    </div>
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
                                                        toEuropeanDate(
                                                            field.value
                                                        )
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
                                            side="bottom"
                                            avoidCollisions={false}
                                        >
                                            <Calendar
                                                mode="single"
                                                selected={field.value}
                                                onSelect={field.onChange}
                                            />
                                        </PopoverContent>
                                    </Popover>
                                ) : (
                                    <Input
                                        value={
                                            field.value
                                                ? toEuropeanDate(field.value)
                                                : ""
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
                        name="paidDate"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Paid Date</FormLabel>
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
                                                        toEuropeanDate(
                                                            field.value
                                                        )
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
                                            side="bottom"
                                            avoidCollisions={false}
                                        >
                                            <Calendar
                                                mode="single"
                                                selected={field.value}
                                                onSelect={field.onChange}
                                            />
                                        </PopoverContent>
                                    </Popover>
                                ) : (
                                    <Input
                                        value={
                                            field.value
                                                ? toEuropeanDate(field.value)
                                                : ""
                                        }
                                        readOnly
                                        className="bg-muted"
                                    />
                                )}
                                <FormMessage />
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
                                onClick={cancelEdit}
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
