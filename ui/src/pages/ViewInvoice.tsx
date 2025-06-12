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
import { useParams, useNavigate } from "react-router-dom";
import { useFetchClient } from "@/hooks/api/client";
import { z } from "zod";
import PdfPreview from "@/components/PdfPreview";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { CalendarIcon, Pencil, Save } from "lucide-react";
import { cn } from "@/lib/utils";
import { useForm } from "react-hook-form";

function ViewInvoice() {
    const { invoiceId } = useParams();
    const [editMode, setEditMode] = useState(false);

    const { invoice, isLoading, error } = useFetchInvoice(invoiceId);
    const { url: invoiceUrl } = useFetchInvoiceUrl(invoiceId);
    const { currencies } = useFetchCurrencies();
    const { client } = useFetchClient(invoice?.clientId);

    const currency =
        currencies?.find((c) => c.id === invoice?.currencyId)?.name || "";

    const invoiceSchema = z.object({
        invoiceNumber: z.string(),
        invoiceDescription: z.string(),
        grossAmount: z.coerce.number().min(0, "Must be positive"),
        currency: z.string(),
        vat: z.coerce.number().min(0).max(50),
        clientName: z.string(),
        invoicedDate: z.date(),
        paidDate: z.date().optional(),
    });

    const form = useForm<z.infer<typeof invoiceSchema>>({
        resolver: zodResolver(invoiceSchema),
        defaultValues: {
            invoiceNumber: invoice?.invoiceNumber || "",
            invoiceDescription: "",
            grossAmount: invoice?.grossAmount || 0,
            vat: invoice?.vat || 0,
            currency: currency,
            clientName: client?.clientName || "",
            invoicedDate: invoice?.issuedDate || new Date(),
            paidDate: new Date(), //Not implemented yet
        },
    });

    const onSubmit = (values: z.infer<typeof invoiceSchema>) => {};

    return (
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
                    <Button
                        variant="outline"
                        onClick={() => setEditMode(!editMode)}
                        className="flex items-center gap-2"
                    >
                        {editMode ? (
                            <>
                                <Save className="w-4 h-4" />
                                <span>Save</span>
                            </>
                        ) : (
                            <>
                                <Pencil className="w-4 h-4" />
                                <span>Edit</span>
                            </>
                        )}
                    </Button>
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
                                        <Input value={field.value} readOnly />
                                    )}
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="invoicedDate"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Invoice Date</FormLabel>
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
                                                className="w-auto p-0"
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
                                            value={format(field.value, "PPP")}
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
    );
}

export default ViewInvoice;
