import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import "../assets/css/footer.css";

function Footer() {
  return (
    <footer className="footer text-light">
      <Container>
        <Row>
          <Col className="text-center py-3">
            &copy; {new Date().getFullYear()} Sarthi. All Rights Reserved.
          </Col>
        </Row>
        <Row>
          <Col className="text-center py-3">
            <a href="/terms" className="text-light">
              Terms & Conditions
            </a>{" "}
            |
            <a href="/privacy" className="text-light mx-2">
              Privacy Policy
            </a>
          </Col>
        </Row>
      </Container>
    </footer>
  );
}

export default Footer;
