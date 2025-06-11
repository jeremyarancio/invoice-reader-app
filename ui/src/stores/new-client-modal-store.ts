import { create } from "zustand";

interface NewClientModalStore {
    isNewClientModalOpen: boolean;
    openNewClientModal: () => void;
    closeNewClientModal: () => void;
}

export const useNewClientModalStore = create<NewClientModalStore>((set) => ({
    isNewClientModalOpen: false,
    openNewClientModal: () => set({ isNewClientModalOpen: true }),
    closeNewClientModal: () => set({ isNewClientModalOpen: false }),
}));
