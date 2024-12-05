export interface Invoice {
    id: number;
    number: string;
    clientName: string;
    date: string;
    revenue: number;
    paid: boolean;
  }

export interface UserRegistrationData {
    username: string;
    email: string;
    password: string;
  }