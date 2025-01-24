import { Button, Card, Container, Row, Col } from "react-bootstrap";
import AuthForm from "./AuthForm";
import { useSignUp } from "./hooks";
import { FormSignUp } from "./types";
import { useNavigate } from "react-router-dom";

function SignUp() {
    const signUp = useSignUp();
    const navigate = useNavigate();

    return (
        <Container className="d-flex justify-content-center align-items-center vh-100">
            <Card className="p-4 shadow" style={{ width: "400px" }}>
                <Card.Body>
                    <h2 className="text-center mb-4">Sign Up</h2>
                    <AuthForm<FormSignUp>
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
                        onSubmit={signUp}
                    />
                    <Row className="mt-3">
                        <Col className="text-center">
                            <p className="mb-2">Already registered?</p>
                            <Button
                                variant="outline-primary"
                                onClick={() => navigate("/signin")}
                                className="w-100"
                            >
                                Sign In
                            </Button>
                        </Col>
                    </Row>
                </Card.Body>
            </Card>
        </Container>
    );
}

export default SignUp;