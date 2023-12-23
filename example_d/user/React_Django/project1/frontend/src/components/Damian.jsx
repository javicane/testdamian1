import React, { useState } from 'react';
import axios from 'axios';

function Damian() {
  const [data, setData] = useState([]);
  const [selectedValues, setSelectedValues] = useState({});
  const [errorMessage, setErrorMessage] = useState('');

  function first_api_call_with_axios(event) {
    axios({
      method: 'POST',
      url: '/with_id/'
    })
      .then(response => {
        setData(response.data);
        const initialSelectedValues = response.data.reduce((acc, item) => {
          acc[item.id] = 'UP'; // Default value for each row
          return acc;
        }, {});
        setSelectedValues(initialSelectedValues);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
    event.preventDefault();
  }

  const handleInputChange = (id, value) => {
    setErrorMessage(''); // Clear error message

    // Validate the input value to allow only numbers (integer or decimal)
    if (value !== '' && !/^\d*\.?\d*$/.test(value)) {
      setErrorMessage('Invalid input value');
      return; // Stop further processing
    }

    const newData = data.map(item => {
      if (item.id === id) {
        return { ...item, inputValue: value };
      }
      return item;
    });

    setData(newData);
  };

  const handleSelectChange = (id, value) => {
    setSelectedValues(prevSelectedValues => ({
      ...prevSelectedValues,
      [id]: value
    }));
  };

  const handleSecondApiCall = (id, inputValue, selectedValue, currentValues) => {
    // Check if the inputValue is numeric
    if (!/^\d*\.?\d*$/.test(inputValue)) {
      setErrorMessage('Invalid input value');
      return; // Stop further processing
    }

    axios({
      method: 'POST',
      url: '/zaraza/',
      data: {
        id: id,
        input: inputValue,
        option: selectedValue,
        otherValues: currentValues
      }
    })
      .then(response => {
        const newValuetoupdate = response.data[0]['order_status'];

        const updatedData = data.map(item => {
          if (item.id === id) {
            return {
              ...item,
              order_status: newValuetoupdate,
              secondApiResponse: response.data, // Store entire response in state
              error: false // Clear error status
            };
          }
          return item;
        });

        setData(updatedData);
        setErrorMessage(''); // Clear error message
      })
      .catch(error => {
        console.error('Error calling second API:', error);
        const updatedDataWithError = data.map(item => {
          if (item.id === id) {
            return {
              ...item,
              error: true // Set error status
            };
          }
          return item;
        });
        setData(updatedDataWithError);
        setErrorMessage('Error calling second API'); // Display error message
      });
  };

  return (
    <div>
      <h1>Table Example</h1>
      <button onClick={first_api_call_with_axios}>Create Post</button>
      <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>order_id</th>
            <th>order_status</th>
            <th>order_id_to_close</th>
            <th>tp</th>
            <th>Input Value</th>
            <th>Options</th>
            <th>Submit</th>
            <th>Second API Response / Error</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.order_id}</td>
              <td>{item.order_status}</td>
              <td>{item.order_id_to_close}</td>
              <td>{item.tp}</td>
              <td>
                <input
                  type="text"
                  value={item.inputValue || ''}
                  onChange={event => handleInputChange(item.id, event.target.value)}
                  onBlur={() => setErrorMessage('')}
                />
              </td>
              <td>
                <select
                  value={selectedValues[item.id] || 'UP'}
                  onChange={event => handleSelectChange(item.id, event.target.value)}
                >
                  <option value="UP">UP</option>
                  <option value="DOWN">DOWN</option>
                </select>
              </td>
              <td>
                <button onClick={() => handleSecondApiCall(item.id, item.inputValue, selectedValues[item.id], {
                  order_id: item.order_id,
                  order_status: item.order_status,
                  order_id_to_close: item.order_id_to_close,
                  tp: item.tp
                })}>
                  Submit
                </button>
              </td>
              <td>
                {item.error ? (
                  <span style={{ color: 'red' }}>{errorMessage}</span>
                ) : (
                  item.secondApiResponse ? JSON.stringify(item.secondApiResponse) : '-'
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Damian;
