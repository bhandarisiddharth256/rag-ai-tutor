import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first");

    const formData = new FormData();
    formData.append("file", file);

    await axios.post("http://localhost:8000/upload", formData);

    alert("PDF uploaded!");
  };

  const sendMessage = async () => {
    if (!query) return;

    const res = await axios.post("http://localhost:8000/chat", {
      query: query,
    });

    setMessages([
      ...messages,
      { role: "user", text: query },
      { role: "bot", text: res.data.answer },
    ]);

    setQuery("");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>RAG AI Tutor 🚀</h1>

      {/* Upload */}
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload}>Upload</button>

      <hr />

      {/* Chat */}
      <div>
        {messages.map((msg, i) => (
          <p key={i}>
            <b>{msg.role}:</b> {msg.text}
          </p>
        ))}
      </div>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;