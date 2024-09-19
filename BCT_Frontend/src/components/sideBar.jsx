import React from "react";
import { Container, Row, Col, Nav, Navbar } from "react-bootstrap";
import "../assets/css/sidebar.css";

function SideBar() {
  return (
    <Container fluid>
      <Row>
        {/* Sidebar Column */}
        <Col xs={3} id="sidebar">
          <Navbar.Brand className="nav-header fs-2">Sarthi</Navbar.Brand>
          <Nav
            defaultActiveKey="/home"
            className="flex-column sidebar-nav fs-5"
          >
            <Nav.Link href="/dashboard" className="text-light">
              Dashboard
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-1" className="text-light">
              Internal Calling
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-2" className="text-light">
              Task Manager
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-3" className="text-light">
              Support Desk
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-4" className="text-light">
              Register Calling Number
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-5" className="text-light">
              Refresh Call Logs
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-6" className="text-light">
              Refer CV
            </Nav.Link>
            <Nav.Link href="#" eventKey="link-7" className="text-light">
              Logout
            </Nav.Link>
          </Nav>
        </Col>
      </Row>
    </Container>
  );
}

export default SideBar;
