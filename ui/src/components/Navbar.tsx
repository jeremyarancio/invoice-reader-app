import { Link } from "react-router-dom";
import { Navbar as BootstrapNavbar, Nav, Container } from "react-bootstrap";

const Navbar = () => (
    <BootstrapNavbar bg="dark" variant="dark" expand="lg">
        <Container>
            <BootstrapNavbar.Brand as={Link} to="/">
                Invoice Manager
            </BootstrapNavbar.Brand>
            <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
            <BootstrapNavbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link as={Link} to="/upload">
                        Upload Invoice
                    </Nav.Link>
                </Nav>
                <Nav>
                    <Nav.Link as={Link} to="/profile">
                        Profile
                    </Nav.Link>
                    <Nav.Link as={Link} to="/login">
                        Login
                    </Nav.Link>
                    <Nav.Link as={Link} to="/register">
                        Register
                    </Nav.Link>
                </Nav>
            </BootstrapNavbar.Collapse>
        </Container>
    </BootstrapNavbar>
);

export default Navbar;
