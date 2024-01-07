import "./Leaderboard.css";
import Table from "react-bootstrap/Table";

const Leaderboard = () => {
  return (
    <>
      <div class="main content">
        <h1 style={{ marginBottom: "2rem" }}> Leaderboard </h1>
        <Table striped hover bordered className="leaderboard">
          <thead>
            <tr>
              <th className="header-row">#</th>
              <th className="header-row">Problem</th>
              <th> Solution</th>
              <th>Score</th>
              <th>Topic</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Sample Problem</td>
              <td>Sample Solution</td>
              <td>25</td>
              <td>ABC</td>
            </tr>
            <tr>
              <td>2 </td>
              <td>Sample Problem</td>
              <td>Sample Solution</td>
              <td>24</td>
              <td>ABC</td>
            </tr>
          </tbody>
        </Table>
      </div>
    </>
  );
};

export default Leaderboard;
