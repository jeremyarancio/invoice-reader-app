import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";

import { CalendarIcon } from "lucide-react";
import { Calendar } from "@/components/ui/calendar";
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
import { Input } from "@/components/ui/input";
import type { ParsedInvoice } from "@/schemas/parser";
import type { Client } from "@/schemas/client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { cn, toEuropeanDate } from "@/lib/utils";
import AppAlert from "@/components/AppAlert";
import { useState } from "react";
import { useIsSubmittedAlert } from "@/hooks/alert-hooks";
import NewClientModal from "./NewClientModal";
import { useNavigate } from "react-router-dom";
import { useAddInvoice } from "@/hooks/api/invoice";
import { CURRENCIES, type InvoiceData } from "@/schemas/invoice";

interface Props {
    file: File;
    clients: Client[];
    parsedInvoice?: ParsedInvoice;
}

function AddInvoiceForm({ file, parsedInvoice, clients }: Props) {
    const [isNewClientModalOpen, setIsNewClientModalOpen] = useState(false);
    const { isSubmitted, setIsSubmitted } = useIsSubmittedAlert();
    const navigate = useNavigate();
    const addInvoice = useAddInvoice();

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        try {
            const invoiceData: InvoiceData = {
                description: values.invoiceDescription,
                grossAmount: values.grossAmount,
                invoiceNumber: values.invoiceNumber,
                issuedDate: values.issuedDate,
                paidDate: values.paidDate,
                vat: values.vat,
                currency: values.currency,
            };
            await addInvoice(file, invoiceData, values.client_id);
            setIsSubmitted(true);
            navigate("/invoices"); //Alert can be improved
        } catch (error) {
            console.error("Error adding invoice:", error);
        }
    };

    const formSchema = z
        .object({
            invoiceNumber: z.string().min(1, "Invoice number is required"),
            invoiceDescription: z
                .string()
                .min(1, "Invoice description is required")
                .max(
                    100,
                    "Invoice description must be less than 100 characters"
                ),
            grossAmount: z.coerce // Number type
                .number()
                .min(0, "Gross amount must be a positive number")
                .max(1000000, "Gross amount must be less than 1,000,000"),
            currency: z.string().min(1, "Currency is required"),
            vat: z.coerce
                .number()
                .min(0, "VAT is required")
                .max(50, "VAT must be less than 50%"),
            client_id: z.string().min(1, "Client is required"),
            issuedDate: z.date({
                required_error: "Issued date is required",
            }),
            paidDate: z.date().optional(),
        })
        .refine((data) => !data.paidDate || data.paidDate >= data.issuedDate, {
            message: "Paid date cannot be before issued date",
            path: ["paidDate"],
        });

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            invoiceNumber: parsedInvoice?.invoice.invoice_number || "",
            invoiceDescription:
                parsedInvoice?.invoice.invoice_description || "",
            grossAmount: parsedInvoice?.invoice.gross_amount || undefined,
            currency: parsedInvoice?.invoice.currency
                ? CURRENCIES[
                      parsedInvoice.invoice.currency as keyof typeof CURRENCIES
                  ]?.symbol || parsedInvoice.invoice.currency
                : undefined,
            vat: parsedInvoice?.invoice.vat || undefined,
            client_id: parsedInvoice?.client_id || "",
            issuedDate: parsedInvoice?.invoice.issued_date
                ? new Date(parsedInvoice.invoice.issued_date)
                : undefined,
            paidDate: undefined,
        },
    });

    return (
        <>
            {isNewClientModalOpen && (
                <NewClientModal
                    isOpen={isNewClientModalOpen}
                    onClose={() => setIsNewClientModalOpen(false)}
                />
            )}
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-8"
                >
                    <FormField
                        control={form.control}
                        name="invoiceNumber"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Invoice Number
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input placeholder="FR0001" {...field} />
                                </FormControl>
                                <FormDescription>
                                    The invoice number should be unique
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="invoiceDescription"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Description
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Consulting services"
                                        {...field}
                                    />
                                </FormControl>
                                <FormDescription>
                                    Brief summary of the completed project.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="grossAmount"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Gross Amount
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="1000"
                                        type="number"
                                        {...field}
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
                                <FormLabel>
                                    Currency
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <Select
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                >
                                    <FormControl>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select a currency." />
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
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="vat"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    VAT (%)
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="21"
                                        type="number"
                                        className="max-w-30"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="client_id"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Client
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <div className="flex gap-2 items-center">
                                    <Select
                                        onValueChange={field.onChange}
                                        defaultValue={field.value}
                                    >
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select a Client" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent className="bg-stone-50">
                                            {clients.map((client) => (
                                                <SelectItem
                                                    key={client.clientName}
                                                    value={client.id}
                                                >
                                                    {client.clientName}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                    <button
                                        className="button-secondary"
                                        type="button"
                                        onClick={() =>
                                            setIsNewClientModalOpen(true)
                                        }
                                    >
                                        New client
                                    </button>
                                </div>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="issuedDate"
                        render={({ field }) => (
                            <FormItem className="flex flex-col">
                                <FormLabel>
                                    Invoiced Date
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <FormControl>
                                            <Button
                                                variant={"outline"}
                                                className={cn(
                                                    "w-[240px] pl-3 text-left font-normal",
                                                    !field.value &&
                                                        "text-muted-foreground"
                                                )}
                                            >
                                                {field.value ? (
                                                    toEuropeanDate(field.value)
                                                ) : (
                                                    <span>Pick a date</span>
                                                )}
                                                <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                            </Button>
                                        </FormControl>
                                    </PopoverTrigger>
                                    <PopoverContent
                                        side="bottom"
                                        avoidCollisions={false}
                                        className="w-auto p-0 bg-stone-50"
                                        align="start"
                                    >
                                        <Calendar
                                            mode="single"
                                            selected={field.value}
                                            onSelect={field.onChange}
                                            disabled={(date) =>
                                                date > new Date() ||
                                                date < new Date("1900-01-01")
                                            }
                                            initialFocus
                                        />
                                    </PopoverContent>
                                </Popover>
                                <FormDescription>
                                    The date when the invoice was issued.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="paidDate"
                        render={({ field }) => (
                            <FormItem className="flex flex-col">
                                <FormLabel>Paid Date</FormLabel>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <FormControl>
                                            <Button
                                                variant={"outline"}
                                                className={cn(
                                                    "w-[240px] pl-3 text-left font-normal",
                                                    !field.value &&
                                                        "text-muted-foreground"
                                                )}
                                            >
                                                {field.value ? (
                                                    toEuropeanDate(field.value)
                                                ) : (
                                                    <span>Pick a date</span>
                                                )}
                                                <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                            </Button>
                                        </FormControl>
                                    </PopoverTrigger>
                                    <PopoverContent
                                        side="bottom"
                                        avoidCollisions={false}
                                        align="start"
                                        className="w-auto p-0 bg-stone-50"
                                    >
                                        <Calendar
                                            mode="single"
                                            selected={field.value}
                                            onSelect={field.onChange}
                                            disabled={(date) =>
                                                date > new Date() ||
                                                date < new Date("1900-01-01")
                                            }
                                        />
                                    </PopoverContent>
                                </Popover>
                                <FormDescription>
                                    The date when the invoice was paid.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <button type="submit" className="button-primary">
                        Add Invoice
                    </button>
                </form>
            </Form>
            {isSubmitted && <AppAlert />}
        </>
    );
}

export default AddInvoiceForm;
