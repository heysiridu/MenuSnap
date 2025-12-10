import React from "react";
import LoadingIcon from "./LoadingIcon";

export default function Processing({ progress = 0 }) {
  return (
    <div style={styles.container}>
      <div style={styles.circle}>
        <LoadingIcon />
      </div>

      <p style={styles.text}>
        Your menu is processing<br />
        {progress}%....
      </p>

      <div style={styles.progressContainer}>
        <div style={styles.progressBar}>
          <div 
            style={{
              ...styles.progressFill,
              width: `${progress}%`
            }}
          />
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    width: "100vw",
    height: "100vh",
    backgroundColor: "#ffffff",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: "20px",
    boxSizing: "border-box",
  },
  circle: {
    width: "220px",
    height: "220px",
    backgroundColor: "#E8ECEF",
    borderRadius: "50%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: "25px",
  },
  text: {
    fontSize: "20px",
    fontWeight: 500,
    textAlign: "center",
    lineHeight: "1.4",
    marginBottom: "20px",
  },
  progressContainer: {
    width: "80%",
    maxWidth: "280px",
  },
  progressBar: {
    width: "100%",
    height: "8px",
    backgroundColor: "#E8ECEF",
    borderRadius: "4px",
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    backgroundColor: "#000",
    borderRadius: "4px",
    transition: "width 0.3s ease",
  },
};
