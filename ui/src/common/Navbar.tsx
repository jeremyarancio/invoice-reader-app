import { Link } from "react-router-dom";
import {
    Navbar as BootstrapNavbar,
    Nav,
    Container,
    Button,
} from "react-bootstrap";
import { useSignOut } from "./hooks";

const Navbar = () => {
    const signOut = useSignOut();

    return (
        <BootstrapNavbar bg="dark" variant="dark" expand="lg">
            <Container>
                <BootstrapNavbar.Brand as={Link} to="/">
                    Invoice Manager
                </BootstrapNavbar.Brand>
                <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
                <BootstrapNavbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/clients">
                            Clients
                        </Nav.Link>
                    </Nav>
                </BootstrapNavbar.Collapse>
                <Button variant="dark" onClick={signOut}>
                    Sign Out
                </Button>
            </Container>
        </BootstrapNavbar>
    );
};

export default Navbar;
