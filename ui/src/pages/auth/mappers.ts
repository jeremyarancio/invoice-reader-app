import { formSignIn, formSignUp, CreateUser, PostUser } from "./types";

export const mapFormSignInToCreateUser = (
    formSignIn: formSignIn
): CreateUser => {
    return {
        email: formSignIn.email,
        password: formSignIn.password,
    };
};

export const mapFormSignUpToPostUser = (formSignUp: formSignUp): PostUser => {
    return {
        email: formSignUp.email,
        password: formSignUp.password,
    };
};
