import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type Currency = 'USD' | 'EUR' | 'GBP' | 'CZK';

interface CurrencyStore {
    selectedCurrency: Currency;
    setSelectedCurrency: (currency: Currency) => void;
}

export const useCurrencyStore = create<CurrencyStore>()(
    persist(
        (set) => ({
            selectedCurrency: 'EUR',
            setSelectedCurrency: (currency) => set({ selectedCurrency: currency }),
        }),
        {
            name: 'currency-storage',
        }
    )
);
