import { FormGroup } from "@/common/types";
import SubmissionForm from "@/common/components/SubmissionForm";

interface AuthProps<T> {
    onSubmit: (data: T) => void;
    formGroups: FormGroup<T>[];
    initialData: T;
}

function AuthForm<T>({ onSubmit, formGroups, initialData }: AuthProps<T>) {
    return (
        <SubmissionForm
            formGroups={formGroups}
            submit={onSubmit}
            initialData={initialData}
        />
    );
}

export default AuthForm;
