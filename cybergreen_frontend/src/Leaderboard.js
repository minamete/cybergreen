import { useEffect, useState } from "react";
import "./Leaderboard.css";
import Table from "react-bootstrap/Table";

const Leaderboard = () => {
  const [dbTable, setDBTable] = useState([]);

  useEffect(() => {
    // load the rows from the db
    try {
      fetch("http://localhost:5000/submission", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        mode: "cors",
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          // set table values and sort table
          setDBTable(
            JSON.parse(data.response).sort((a, b) => (a.scores.overall_score > b.scores.overall_score ? -1 : 1))
          );
        });
    } catch (error) {
      console.error("DB loading failed", error);
    }
  }, []);

  return (
    <>
      <div className="main content">
        <h1 style={{ marginBottom: "2rem" }}> Leaderboard </h1>
        <Table striped hover bordered className="leaderboard">
          <thead>
            <tr>
              <th className="header-row">#</th>
              <th className="header-row">Problem</th>
              <th className="header-row">Solution</th>
              <th className="header-row">Overall Score</th>
              <th className="header-row">Impact</th>
              <th className="header-row">Feasibility</th>
              <th className="header-row">Novelty</th>
            </tr>
          </thead>
          <tbody>
            {dbTable.map((dbRow, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td className="problem-cell">{dbRow.problem}</td>
                <td className="solution-cell">{dbRow.solution}</td>
                <td>{dbRow.scores.overall_score}</td>
                <td>{dbRow.scores.env_impact_score}</td>
                <td>{dbRow.scores.feasibility_score}</td>
                <td>{dbRow.scores.novelty_score}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </>
  );
};

export default Leaderboard;
