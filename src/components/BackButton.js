import React from 'react';
import { useNavigate } from 'react-router-dom';

const BackButton = () => {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate(-1); // Navigates back to the previous page in history
  };

  return (
    <button onClick={handleBack}>Back</button>
  );
};

export default BackButton;
