import { NavLink } from "react-router-dom";
import {
    Navbar as BootstrapNavbar,
    Nav,
    Button,
    Container,
} from "react-bootstrap";
import { useSignOut } from "./hooks";

const Navbar = () => {
    const signOut = useSignOut();

    return (
        <BootstrapNavbar bg="dark" variant="dark" expand="lg">
            <Container>
                <BootstrapNavbar.Brand as={NavLink} to="/">
                    Invoice Manager
                </BootstrapNavbar.Brand>
                <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
                <BootstrapNavbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={NavLink} to="/clients">
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
