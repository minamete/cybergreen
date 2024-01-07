import React, { useState } from 'react';

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

    // Additional verification for CSV format (you can customize this based on your specific format)
    // For example, check if the CSV file has a specific header or structure

    setError(null);
    setCsvFile(file);
  };

  const handleSubmit = () => {
    

    console.log('Submitted CSV file:', csvFile);
  };

  return (
    <div>
    <p>
        Or...submit several problems and solutions here! (please upload your file in .csv format)
    </p>
      <input type="file" onChange={handleFileChange} />
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <button onClick={handleSubmit} disabled={!csvFile}>
        Submit
      </button>
    </div>
  );
};

export default CsvFileUploader;
