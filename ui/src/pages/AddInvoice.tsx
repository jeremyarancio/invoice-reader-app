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
import { format } from "date-fns";
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
import { ArrowLeft } from "lucide-react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { cn, toDate } from "@/lib/utils";
import AppAlert from "@/components/AppAlert";
import { useNavigate, useLocation } from "react-router-dom";
import PdfPreview from "@/components/PdfPreview";
import NewClientModal from "@/components/NewClientModal";
import { useIsSubmittedAlert } from "@/hooks/alert-hooks";
import { useAddInvoice, useFetchCurrencies } from "@/hooks/api/invoice";
import { useFetchClients } from "@/hooks/api/client";
import { useNewClientModalStore } from "@/stores/new-client-modal-store";

function AddInvoice() {
    const navigate = useNavigate();
    const file = useLocation().state?.file;
    const { isSubmitted, setIsSubmitted } = useIsSubmittedAlert();
    const addInvoice = useAddInvoice();
    const fetchClients = useFetchClients();
    const fetchCurrencies = useFetchCurrencies();
    const { isNewClientModalOpen, openNewClientModal, closeNewClientModal } =
        useNewClientModalStore();

    const formSchema = z.object({
        invoiceNumber: z.string().min(1, "Invoice number is required"),
        invoiceDescription: z
            .string()
            .min(1, "Invoice description is required")
            .max(100, "Invoice description must be less than 100 characters"),
        grossAmount: z.coerce // Number type
            .number()
            .min(0, "Gross amount must be a positive number")
            .max(1000000, "Gross amount must be less than 1,000,000"),
        currency_id: z.string(),
        vat: z.coerce.number().min(0).max(50),
        client_id: z.string(),
        invoicedDate: z.date(),
        paidDate: z.date().optional(),
    });

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
    });

    const { clients } = fetchClients();

    const { currencies } = fetchCurrencies();

    const onSubmit = (values: z.infer<typeof formSchema>) => {
        addInvoice(file, {
            client_id: values.client_id,
            currency_id: values.currency_id,
            invoice: {
                amount_excluding_tax: values.grossAmount,
                invoice_number: values.invoiceNumber,
                invoiced_date: toDate(values.invoicedDate),
                is_paid: !!values.paidDate,
                vat: values.vat,
            },
        });
        setIsSubmitted(true);
        navigate("/invoices"); //Alert can be improved
    };

    return (
        <>
            {isNewClientModalOpen && (
                <NewClientModal
                    isOpen={isNewClientModalOpen}
                    onClose={() => closeNewClientModal}
                />
            )}
            <div className="mt-10 ml-10">
                <button
                    onClick={() => navigate("/invoices")}
                    className="hover:cursor-pointer"
                >
                    <ArrowLeft
                        size={40}
                        className="rounded-full hover:bg-stone-50"
                    />
                </button>
            </div>
            <div className="flex mt-20 mb-40 justify-around">
                <div className="px-4 flex justify-center">
                    <PdfPreview file={file} />
                </div>
                <div className="px-4 md:px-20 w-full">
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
                                            <span className="text-red-600">
                                                *
                                            </span>
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="FR0001"
                                                {...field}
                                            />
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
                                            <span className="text-red-600">
                                                *
                                            </span>
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="Consulting services"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            Brief summary of the completed
                                            project.
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
                                            <span className="text-red-600">
                                                *
                                            </span>
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
                                name="currency_id"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>
                                            Currency
                                            <span className="text-red-600">
                                                *
                                            </span>
                                        </FormLabel>
                                        <Select
                                            onValueChange={field.onChange}
                                            defaultValue={field.name}
                                        >
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select a currency." />
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
                                            <span className="text-red-600">
                                                *
                                            </span>
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
                                            <span className="text-red-600">
                                                *
                                            </span>
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
                                                            key={
                                                                client.clientName
                                                            }
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
                                                onClick={openNewClientModal}
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
                                name="invoicedDate"
                                render={({ field }) => (
                                    <FormItem className="flex flex-col">
                                        <FormLabel>
                                            Invoiced Date
                                            <span className="text-red-600">
                                                *
                                            </span>
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
                                                            format(
                                                                field.value,
                                                                "PPP"
                                                            )
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
                                                className="w-auto p-0 bg-stone-50"
                                                align="start"
                                            >
                                                <Calendar
                                                    mode="single"
                                                    selected={field.value}
                                                    onSelect={field.onChange}
                                                    disabled={(date) =>
                                                        date > new Date() ||
                                                        date <
                                                            new Date(
                                                                "1900-01-01"
                                                            )
                                                    }
                                                    initialFocus
                                                />
                                            </PopoverContent>
                                        </Popover>
                                        <FormDescription>
                                            The date when the invoice was
                                            issued.
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
                                                            format(
                                                                field.value,
                                                                "PPP"
                                                            )
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
                                                className="w-auto p-0 bg-stone-50"
                                                align="start"
                                            >
                                                <Calendar
                                                    mode="single"
                                                    selected={field.value}
                                                    onSelect={field.onChange}
                                                    disabled={(date) =>
                                                        date > new Date() ||
                                                        date <
                                                            new Date(
                                                                "1900-01-01"
                                                            )
                                                    }
                                                    initialFocus
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
                </div>
            </div>
            {isSubmitted && <AppAlert />}
        </>
    );
}

export default AddInvoice;
