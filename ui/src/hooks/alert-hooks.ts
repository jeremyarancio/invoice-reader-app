//Hooks to trigger alerts

import { useState } from "react";

export const useIsSubmittedAlert = () => {
    const [isSubmitted, setIsSubmitted] = useState(false);
    return { isSubmitted, setIsSubmitted };
};
