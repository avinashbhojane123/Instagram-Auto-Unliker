

import React, { useState, useEffect } from "react";
import axios from "axios";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer, toast } from "react-toastify";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [logs, setLogs] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [unlikedCount, setUnlikedCount] = useState(0);
  const [darkMode, setDarkMode] = useState(true);

  const startUnliker = async () => {
    try {
      await axios.post("http://localhost:5000/start", {
        username,
        password,
        unlikeDelay: 1,
        recheckDelay: 10,
      });
      setIsRunning(true);
      toast.success("Unliker started successfully");
    } catch (err) {
      toast.error("Failed to start: " + err.message);
    }
  };

  const stopUnliker = async () => {
    try {
      await axios.post("http://localhost:5000/stop");
      setIsRunning(false);
      toast.info("Unliker stopped");
    } catch (err) {
      toast.error("Failed to stop: " + err.message);
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await axios.get("http://localhost:5000/logs");
      setLogs(res.data.logs);
      setUnlikedCount(res.data.unliked_count || 0);
    } catch (err) {
      console.error("Error fetching logs:", err);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  const toggleTheme = () => setDarkMode(!darkMode);

  const styles = {
    container: {
      fontFamily: "Segoe UI, sans-serif",
      padding: 20,
      background: darkMode ? "#141e30" : "#f0f0f0",
      minHeight: "100vh",
      color: darkMode ? "#fff" : "#000",
      transition: "all 0.3s ease",
    },
    card: {
      background: darkMode ? "#1e2a3a" : "#fff",
      borderRadius: 12,
      padding: 30,
      maxWidth: 600,
      margin: "auto",
      boxShadow: "0 4px 20px rgba(0,0,0,0.2)",
    },
    title: {
      fontSize: 26,
      textAlign: "center",
      marginBottom: 20,
      fontWeight: "bold",
    },
    input: {
      width: "100%",
      padding: "10px 14px",
      margin: "8px 0",
      borderRadius: 6,
      border: "1px solid #ccc",
      outline: "none",
      fontSize: 16,
    },
    buttonGroup: {
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "space-between",
      marginTop: 20,
    },
    button: (disabled, isPrimary) => ({
      flex: 1,
      margin: "5px",
      padding: "10px 0",
      fontSize: 16,
      borderRadius: 6,
      border: "none",
      background: disabled
        ? "#aaa"
        : isPrimary
        ? "linear-gradient(to right, #00c6ff, #0072ff)"
        : "linear-gradient(to right, #ff512f, #dd2476)",
      color: "#fff",
      cursor: disabled ? "not-allowed" : "pointer",
    }),
    toggleBtn: {
      marginTop: 10,
      padding: "8px 16px",
      fontSize: 14,
      borderRadius: 6,
      background: "#444",
      color: "#fff",
      border: "none",
      cursor: "pointer",
    },
    stats: {
      marginTop: 20,
      fontSize: 18,
      fontWeight: "bold",
      color: "#00e676",
    },
    logsContainer: {
      marginTop: 30,
    },
    logsTitle: {
      fontSize: 18,
      marginBottom: 10,
    },
    logs: {
      background: darkMode ? "#111" : "#eee",
      padding: 15,
      borderRadius: 6,
      height: 250,
      overflowY: "auto",
      fontFamily: "monospace",
      fontSize: 14,
      color: darkMode ? "#00ffcc" : "#000",
    },
  };

  return (
    <div style={styles.container}>
      <ToastContainer position="top-right" autoClose={3000} />
      <div style={styles.card}>
        <div style={styles.title}>📸 Instagram Auto Unliker</div>
        <button onClick={toggleTheme} style={styles.toggleBtn}>
          Toggle {darkMode ? "Light" : "Dark"} Mode
        </button>
        <input
          style={styles.input}
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          style={styles.input}
          placeholder="Enter your password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <div style={styles.buttonGroup}>
          <button
            onClick={startUnliker}
            disabled={isRunning}
            style={styles.button(isRunning, true)}
          >
            ▶ Start
          </button>
          <button
            onClick={stopUnliker}
            disabled={!isRunning}
            style={styles.button(!isRunning, false)}
          >
            ⏹ Stop
          </button>
        </div>
        <div style={styles.stats}>✅ Unliked Posts: {unlikedCount}</div>
        <div style={styles.logsContainer}>
          <h4 style={styles.logsTitle}>📜 Logs:</h4>
          <div style={styles.logs}>
            {logs.length > 0 ? (
              logs.map((log, idx) => <div key={idx}>👉 {log}</div>)
            ) : (
              <div>No logs available yet.</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;