import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { useFetchClient } from "@/hooks/api/client";
import { useNavigate, useParams } from "react-router-dom";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState, useEffect } from "react";
import { Pencil, Save, X } from "lucide-react";
import { useForm } from "react-hook-form";

function ViewClient() {
    const { clientId } = useParams();
    const navigate = useNavigate();
    const [editMode, setEditMode] = useState(false);
    const { client, isLoading } = useFetchClient(clientId);

    const clientSchema = z.object({
        clientName: z.string().min(1, "Client name is required"),
        streetNumber: z.coerce.number().min(1, "Street number is required"),
        streetAddress: z.string().min(1, "Street address is required"),
        zipcode: z.coerce.number().min(1, "Zipcode is required"),
        city: z.string().min(1, "City is required"),
        country: z.string().min(1, "Country is required"),
    });

    const form = useForm<z.infer<typeof clientSchema>>({
        resolver: zodResolver(clientSchema),
    });

    const onSubmit = (values: z.infer<typeof clientSchema>) => {};

    useEffect(() => {
        if (client) {
            form.setValue("clientName", client.clientName);
            form.setValue("streetNumber", client.streetNumber);
            form.setValue("streetAddress", client.streetAddress);
            form.setValue("zipcode", client.zipcode);
            form.setValue("city", client.city);
            form.setValue("country", client.country);
        }
    }, [client, form]);

    const handleCancelEdit = () => {
        if (client) {
            form.reset({
                clientName: client.clientName,
                streetNumber: client.streetNumber,
                streetAddress: client.streetAddress,
                zipcode: client.zipcode,
                city: client.city,
                country: client.country,
            });
            setEditMode(false);
        }
    };

    if (isLoading) {
        return <div className="flex justify-center mt-20">Loading...</div>;
    }

    if (!client && !isLoading) {
        return (
            <div className="flex justify-center mt-20">Client not found</div>
        );
    }

    return (
        <div className="flex flex-col mt-20 mb-40 px-4 md:px-20 max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Client Details</h1>
                <div className="flex gap-2">
                    <Button
                        variant="outline"
                        onClick={() => navigate("/clients")}
                    >
                        Back to Clients
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

            <div className="p-6 rounded-lg border shadow-sm">
                <Form {...form}>
                    <form className="space-y-6">
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
                                            className={
                                                !editMode ? "bg-muted" : ""
                                            }
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
                                                type="number"
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
            </div>

            {/* Revenue Information Section */}
            <div className="bg-card p-6 rounded-lg border shadow-sm mt-6">
                <h2 className="text-xl font-semibold mb-4">
                    Revenue Information
                </h2>
                <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">
                        Total Revenue:
                    </span>
                    <span className="font-semibold text-lg">
                        {client?.totalRevenu || 0} €
                    </span>
                </div>
            </div>

            {/* Client Invoices Section */}
            <div className="bg-card p-6 rounded-lg border shadow-sm mt-6">
                <h2 className="text-xl font-semibold mb-4">Client Invoices</h2>
                <p className="text-muted-foreground">
                    No invoices found for this client.
                </p>
            </div>
        </div>
    );
}

export default ViewClient;
