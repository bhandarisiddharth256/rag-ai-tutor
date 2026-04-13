import { useEffect } from "react";
import axios from "axios";

function App() {

  useEffect(() => {
    axios.get("http://localhost:8000/")
      .then(res => console.log(res.data))
      .catch(err => console.log(err));
  }, []);

  return <h1>RAG AI Tutor 🚀</h1>;
}

export default App;