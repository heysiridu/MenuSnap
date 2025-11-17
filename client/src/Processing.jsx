import React from "react";
import LoadingIcon from "./LoadingIcon";
// import "./processing.css"; // optional, depends on whether to write the css file

export default function Processing() {
  return (
    <div style={styles.container}>
      <div style={styles.circle}>
        <LoadingIcon />
      </div>

      <p style={styles.text}>
        Your menu is processing <br />
        85%....
      </p>
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
  },
};
