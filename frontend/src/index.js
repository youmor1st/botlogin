import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

// точка входа фронтенда
const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);



