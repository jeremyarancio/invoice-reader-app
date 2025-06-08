import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useSignUp } from "@/hooks/api/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";

function SignUp() {
    const navigate = useNavigate();
    const signUp = useSignUp();

    const formSchema = z
        .object({
            email: z.string().email("Please enter a valid email"),
            password: z
                .string()
                .min(8, "Password must be at least 8 characters")
                .regex(/[A-Z]/, "Must contain at least one uppercase letter")
                .regex(/[0-9]/, "Must contain at least one number"),
            confirmPassword: z.string(),
        })
        .refine((data) => data.password === data.confirmPassword, {
            message: "Passwords don't match",
            path: ["confirmPassword"], // This shows the error on confirmPassword field
        });

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        signUp(values);
    }

    return (
        <div className="space-y-6">
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-6"
                >
                    <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Email</FormLabel>
                                <FormControl>
                                    <Input
                                        {...field}
                                        type="email"
                                        placeholder="@"
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Password</FormLabel>
                                <FormControl>
                                    <Input {...field} type="password" />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="confirmPassword"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Confirm Password</FormLabel>
                                <FormControl>
                                    <Input {...field} type="password" />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex justify-center">
                        <button type="submit" className="button-primary">
                            Sign Up
                        </button>
                    </div>
                </form>
            </Form>

            <div className="text-center text-sm text-gray-500">
                <p>
                    Already have an account?{" "}
                    <span
                        onClick={() => navigate("/signin")}
                        className="text-blue-600 hover:underline cursor-pointer"
                    >
                        Sign in
                    </span>
                </p>
            </div>
        </div>
    );
}

export default SignUp;
