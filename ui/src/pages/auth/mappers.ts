import { FormSignIn, FormSignUp, CreateUser, PostUser } from "./types";

export const mapFormSignInToCreateUser = (
    FormSignIn: FormSignIn
): CreateUser => {
    return {
        email: FormSignIn.email,
        password: FormSignIn.password,
    };
};

export const mapFormSignUpToPostUser = (FormSignUp: FormSignUp): PostUser => {
    return {
        email: FormSignUp.email,
        password: FormSignUp.password,
    };
};
