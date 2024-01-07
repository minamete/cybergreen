import React, { useState } from 'react';
import Papa from 'papaparse';
import axios from 'axios';

const CsvFileUploader = () => {
  const [csvFile, setCsvFile] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    // Verify if a file is selected
    if (!file) {
      setError('Please select a file.');
      return;
    }

    // Verify if the selected file is a CSV file
    if (!file.name.endsWith('.csv')) {
      setError('Please select a valid CSV file.');
      return;
    }

    setError(null);
    setCsvFile(file);
  };

  const handleParseCsv = () => {
    // Use papaparse to parse the CSV file
    Papa.parse(csvFile, {
      header: true,
      complete: (result) => {
        // Extract values from columns 2 and 3 for each row
        const parsedData = result.data.map((row) => ({
          problem: row['problem'], // Replace 'Column2' with the actual header of the second column
          solution: row['solution'], // Replace 'Column3' with the actual header of the third column
        }));
  
        console.log('Parsed CSV data:', parsedData);
  
        // Now, make an asynchronous call outside the synchronous block
        sendParsedDataToBackend(parsedData);
      },
      error: (err) => {
        console.error('Error parsing CSV:', err.message);
      },
    });
  };
  
  const sendParsedDataToBackend = async (parsedData) => {
    try {
      // Send a POST request to the Flask backend with the parsed data
      const response = await axios.post('http://localhost:5000/process_csv', { data: parsedData });
      console.log(response.data);
      // Handle the response if needed
    } catch (error) {
      console.error('Error sending data to Flask backend:', error.message);
    }
  };
  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <button onClick={handleParseCsv} disabled={!csvFile}>
        Submit
      </button>
    </div>
  );
};

export default CsvFileUploader;
