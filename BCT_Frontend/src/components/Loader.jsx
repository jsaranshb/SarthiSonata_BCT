import Spinner from "react-bootstrap/Spinner";

function Loader() {
  return (
    <div className="loader-container">
      <Spinner animation="grow" variant="primary" />
      <Spinner animation="grow" variant="secondary" />
      <Spinner animation="grow" variant="success" />
      <Spinner animation="grow" variant="danger" />
      <Spinner animation="grow" variant="warning" />
      <Spinner animation="grow" variant="info" />
    </div>
  );
}
export default Loader;
