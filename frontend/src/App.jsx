import React, { useState, useRef, useEffect } from "react";
import MenuSnapHome from "./components/MenuSnapHome.jsx";
import Processing from "./components/Processing.jsx";
import Results from "./components/Results.jsx";

// const API_BASE_URL = "http://localhost:5001";
const API_BASE_URL = 'http://192.168.1.37:5001';

export default function App() {
  const [currentPage, setCurrentPage] = useState("home");
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [progress, setProgress] = useState(0);
  
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);
  const progressIntervalRef = useRef(null);
  const currentProgressRef = useRef(0);

  const startProgressSimulation = (targetProgress, duration = 3000) => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
    }
    
    const startProgress = currentProgressRef.current;
    const totalSteps = duration / 100;
    const increment = (targetProgress - startProgress) / totalSteps;
    
    progressIntervalRef.current = setInterval(() => {
      currentProgressRef.current += increment;
      if (currentProgressRef.current >= targetProgress) {
        currentProgressRef.current = targetProgress;
        clearInterval(progressIntervalRef.current);
      }
      setProgress(Math.round(currentProgressRef.current));
    }, 100);
  };

  const stopProgressSimulation = () => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
      progressIntervalRef.current = null;
    }
  };

  const finishProgress = async () => {
    stopProgressSimulation();
    const startFrom = Math.round(currentProgressRef.current);
    for (let i = startFrom; i <= 100; i += 3) {
      currentProgressRef.current = i;
      setProgress(i);
      await new Promise(resolve => setTimeout(resolve, 25));
    }
    currentProgressRef.current = 100;
    setProgress(100);
  };

  useEffect(() => {
    return () => stopProgressSimulation();
  }, []);

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const previewUrl = URL.createObjectURL(file);
    setPreviewImage(previewUrl);
    setCurrentPage("processing");
    currentProgressRef.current = 0;
    setProgress(0);
    
    await processImage(file);
  };

  const processImage = async (file) => {
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      startProgressSimulation(85, 20000);
      
      const response = await fetch(`${API_BASE_URL}/api/upload-and-process`, {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        await finishProgress();
        setResults(data);
        setCurrentPage("results");
      } else {
        stopProgressSimulation();
        setError(data.error || 'Failed to process image');
        setCurrentPage("home");
      }
    } catch (err) {
      stopProgressSimulation();
      console.error('API Error:', err);
      setError('Failed to connect to server. Make sure the backend is running on port 5001.');
      setCurrentPage("home");
    }
  };

  const handleDemoClick = async () => {
    setCurrentPage("processing");
    currentProgressRef.current = 0;
    setProgress(0);
    setPreviewImage(null);
    setError(null);
    setResults(null);

    try {
      startProgressSimulation(85, 20000);
      
      const response = await fetch(`${API_BASE_URL}/api/menu/ocr-with-images`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename: 'menu2.png' }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        await finishProgress();
        setResults(data);
        setCurrentPage("results");
      } else {
        stopProgressSimulation();
        setError(data.error || 'Failed to process demo image');
        setCurrentPage("home");
      }
    } catch (err) {
      stopProgressSimulation();
      console.error('API Error:', err);
      setError('Failed to connect to server. Make sure the backend is running on port 5001.');
      setCurrentPage("home");
    }
  };

  const handleGalleryClick = () => {
    fileInputRef.current?.click();
  };

  const handleCameraClick = () => {
    cameraInputRef.current?.click();
  };

  const handleGoHome = () => {
    stopProgressSimulation();
    setCurrentPage("home");
    setResults(null);
    setError(null);
    setPreviewImage(null);
    currentProgressRef.current = 0;
    setProgress(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (cameraInputRef.current) cameraInputRef.current.value = '';
  };

  return (
    <>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept="image/*"
        className="hidden"
      />
      <input
        type="file"
        ref={cameraInputRef}
        onChange={handleFileSelect}
        accept="image/*"
        capture="environment"
        className="hidden"
      />
      
      {currentPage === "home" && (
        <MenuSnapHome
          onPickFromGallery={handleGalleryClick}
          onOpenCamera={handleCameraClick}
          onOpenDemo={handleDemoClick}
          error={error}
        />
      )}
      
      {currentPage === "processing" && (
        <Processing progress={progress} />
      )}
      
      {currentPage === "results" && (
        <Results
          results={results}
          previewImage={previewImage}
          onScanAnother={handleGoHome}
          onNewScan={handleGalleryClick}
        />
      )}
    </>
  );
}
