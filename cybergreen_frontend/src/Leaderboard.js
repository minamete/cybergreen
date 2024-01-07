import { useEffect, useState } from "react";
import "./Leaderboard.css";
import Table from "react-bootstrap/Table";

const Leaderboard = () => {
  useEffect(() => {
    if (numberOfRowsOnPage === 0) return;

    dbTablePages = [];
    setCurrentPage(0);
    let overallCt = 0;

    for (let i = 0; i < dbTable.length / numberOfRowsOnPage; i++) {
      dbTablePages.push([]);
      for (let j = 0; j < numberOfRowsOnPage; j++) {
        if (overallCt >= dbTable.length) return;
        dbTablePages[i].push(dbTable[overallCt]);
        overallCt++;
      }
    }
  }, [numberOfRowsOnPage]);

  const [dbTable, setDBTable] = useState([]);
  const [dbTablePages, setDBTablePages] = useState([]);
  const [numberOfRowsOnPage, setNumberOfRowsOnPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(0);

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
            JSON.parse(data.response)
              .sort((a, b) => (a.score > b.score ? -1 : 1))
              .map((e, i) => {
                return {
                  ...e,
                  indx: i + 1,
                };
              })
          );

          // this is to truncate the table when necessary
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
              <th className="header-row">Score</th>
            </tr>
          </thead>
          <tbody>
            {}
            {dbTable.map((dbRow, index) => (
              <tr key={dbRow.indx}>
                <td>{dbRow.indx}</td>
                <td className="problem-cell">{dbRow.problem}</td>
                <td className="solution-cell">{dbRow.solution}</td>
                <td className="score-cell">{dbRow.score}</td>
              </tr>
            ))}
          </tbody>
        </Table>{" "}
      </div>
    </>
  );
};

export default Leaderboard;
