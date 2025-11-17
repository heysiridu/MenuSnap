import React from "react";
import loadingIcon from "./loading-icon.svg";

export default function LoadingIcon() {
  return (
    <img
      src={loadingIcon}
      alt="loading icon"
      style={{ width: "60px", height: "60px" }}
    />
  );
}
