import React, { useState } from 'react';
import Papa from 'papaparse';
import axios from 'axios';
import './Upload.css'; // Import the CSS file

const CsvFileUploader = () => {
  const [csvFile, setCsvFile] = useState(null);
  const [error, setError] = useState(null);
  const [showDownloadButton, setShowDownloadButton] = useState(false);

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
    setShowDownloadButton(false); // Hide the download button when a new file is selected
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
      const response = await axios.post('http://localhost:5000/process_csv', parsedData);
      console.log(response.data);

      // Now, trigger the download of the updated dataset
      setShowDownloadButton(true); // Show the download button after successful parsing
    } catch (error) {
      console.error('Error sending data to Flask backend:', error.message);
    }
  };

  const handleDownloadUpdatedDataset = async () => {
    try {
      // Send a GET request to the Flask backend to get the download link for the updated dataset
      const response = await axios.get('http://localhost:5000/download_updated_dataset', {
        responseType: 'blob', // Specify the response type as blob
      });

      // Create a link element and simulate a click to trigger the download
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(new Blob([response.data]));
      link.download = 'updated_dataset.csv';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading updated dataset:', error.message);
    }
  };

  return (
    <div className="csv-file-uploader-container">
      <input type="file" onChange={handleFileChange} />
      {error && <div className="error-message">{error}</div>}
      <button onClick={handleParseCsv} disabled={!csvFile}>
        Submit
      </button>
      {showDownloadButton && (
        <button onClick={handleDownloadUpdatedDataset} className="download">
          Download Data Insights
        </button>
      )}
    </div>
  );
};

export default CsvFileUploader;
