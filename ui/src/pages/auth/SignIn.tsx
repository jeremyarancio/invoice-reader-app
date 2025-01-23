import { Button, Container, Card, Row, Col } from "react-bootstrap";
import AuthForm from "./AuthForm";
import { useSignIn } from "./hooks";
import { FormSignIn } from "./types";
import { useNavigate } from "react-router-dom";

function SignIn() {
    const signIn = useSignIn();
    const navigate = useNavigate();

    return (
        <Container className="d-flex justify-content-center align-items-center vh-100">
            <Card className="p-4 shadow" style={{ width: "400px" }}>
                <Card.Body>
                    <h2 className="text-center mb-4">Sign In</h2>
                    <AuthForm<FormSignIn>
                        formGroups={[
                            {
                                header: "Email",
                                key: "email",
                                formType: "email",
                                required: true,
                            },
                            {
                                header: "Password",
                                key: "password",
                                formType: "password",
                                required: true,
                            },
                        ]}
                        initialData={{ email: "", password: "" }}
                        onSubmit={signIn}
                    />
                    <Row className="mt-3">
                        <Col className="text-center">
                            <p className="mb-2">Not registered yet?</p>
                            <Button
                                variant="outline-primary"
                                onClick={() => navigate("/signup")}
                                className="w-100"
                            >
                                Create an Account
                            </Button>
                        </Col>
                    </Row>
                </Card.Body>
            </Card>
        </Container>
    );
}

export default SignIn;
