import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "./ui/input";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import type { Client } from "@/schemas/client";
import { useState } from "react";
import { Pencil, Save, X } from "lucide-react";
import { useUpdateClient } from "@/hooks/api/client";

interface Props {
    client: Client;
}

function ViewClientForm({ client }: Props) {
    const [editMode, setEditMode] = useState(false);
    const updateClient = useUpdateClient();

    const clientSchema = z.object({
        clientName: z.string().min(1, "Client name is required"),
        streetNumber: z.coerce.string().min(1, "Street number is required"),
        streetAddress: z.string().min(1, "Street address is required"),
        zipcode: z.coerce.string().min(1, "Zipcode is required"),
        city: z.string().min(1, "City is required"),
        country: z.string().min(1, "Country is required"),
    });

    const form = useForm<z.infer<typeof clientSchema>>({
        resolver: zodResolver(clientSchema),
        defaultValues: {
            clientName: client.clientName,
            streetNumber: client.streetNumber,
            streetAddress: client.streetAddress,
            zipcode: client.zipcode,
            city: client.city,
            country: client.country,
        },
    });

    // We can keep this function for future use
    const cancelEdit = () => {
        form.reset(client);
        setEditMode(false);
    };

    const onSubmit = async (values: z.infer<typeof clientSchema>) => {
        try {
            await updateClient(client.id, {
                clientName: values.clientName,
                streetNumber: values.streetNumber,
                streetAddress: values.streetAddress,
                zipcode: values.zipcode,
                city: values.city,
                country: values.country,
            });
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
                        name="clientName"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Client Name</FormLabel>
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

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <FormField
                            control={form.control}
                            name="streetNumber"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Street Number</FormLabel>
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
                            name="streetAddress"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Street Address</FormLabel>
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
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <FormField
                            control={form.control}
                            name="zipcode"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Zipcode</FormLabel>
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
                            name="city"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>City</FormLabel>
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
                            name="country"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Country</FormLabel>
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
                    </div>
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

export default ViewClientForm;
