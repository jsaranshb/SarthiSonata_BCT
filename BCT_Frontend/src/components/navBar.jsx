import Container from "react-bootstrap/Container";
import { Navbar, NavDropdown } from "react-bootstrap";
import "../assets/css/navbar.css";

function NavBar() {
  return (
    <Navbar className="nav-container">
      <Container>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <NavDropdown title="Dropdown" id="basic-nav-dropdown">
            <NavDropdown.Item>User ID: </NavDropdown.Item>
            <NavDropdown.Item>User name: </NavDropdown.Item>
            <NavDropdown.Item>Role Name: </NavDropdown.Item>
            <NavDropdown.Item>Region Head: </NavDropdown.Item>
            <NavDropdown.Item>Last Login: </NavDropdown.Item>
            <NavDropdown.Item>mobile No: </NavDropdown.Item>
          </NavDropdown>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
