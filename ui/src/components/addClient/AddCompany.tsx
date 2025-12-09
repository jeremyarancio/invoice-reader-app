import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useIsSubmittedAlert } from "@/hooks/alert-hooks";
import { useAddClient } from "@/hooks/api/client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

interface Props {
    onSuccess?: () => void;
    onError?: () => void;
}

function AddCompany({ onSuccess, onError }: Props) {
    const { setIsSubmitted } = useIsSubmittedAlert();
    const addClient = useAddClient({ onSuccess: onSuccess, onError: onError });

    const formSchema = z.object({
        client_name: z.string(),
        street_number: z.string(),
        street_address: z.string(),
        zipcode: z.string(),
        city: z.string(),
        country: z.string(),
        vatNumber: z.coerce.string(),
    });

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        setIsSubmitted(true);
        addClient(values);
    }

    return (
        <>
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-8"
                >
                    <FormField
                        control={form.control}
                        name="client_name"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Company's name
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormDescription>
                                    The client name should be unique.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="street_number"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Address number
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input {...field} type="number" />
                                </FormControl>
                                <FormDescription></FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="street_address"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Address
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormDescription></FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="zipcode"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Zipcode
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="city"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    City
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="country"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>
                                    Country
                                    <span className="text-red-600">*</span>
                                </FormLabel>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="vatNumber"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>VAT</FormLabel>
                                <FormDescription>
                                    Company VAT number if exists.
                                </FormDescription>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <button type="submit" className="button-primary">
                        Add Client
                    </button>
                </form>
            </Form>
        </>
    );
}

export default AddCompany;
