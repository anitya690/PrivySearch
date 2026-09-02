import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [backendStatus, setBackendStatus] = useState("");

  const checkBackend = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/health");
      const data = await response.json();

      setBackendStatus(`${data.service} is ${data.status}`);
    } catch (error) {
      setBackendStatus("Backend connection failed");
      console.error(error);
    }
  };

 const [results, setResults] = useState([]);
const [loading, setLoading] = useState(false);
const [searchError, setSearchError] = useState("");

const handleSearch = async (e) => {
  e.preventDefault();

  if (!query.trim()) return;

  setLoading(true);
  setSearchError("");
  setResults([]);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/search?query=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      throw new Error("Search request failed");
    }

    const data = await response.json();

    setResults(data.results);
  } catch (error) {
    console.error(error);
    setSearchError("Unable to connect to the search service.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🔐</span>
          <span>PrivySearch</span>
        </div>

        <button className="privacy-btn" onClick={checkBackend}>
          🛡️ Check API
        </button>
      </header>

      <main className="main">
        <div className="hero">
          <div className="brand-icon">🔎</div>

          <h1>
            Search <span>without profiling.</span>
          </h1>

          <p className="subtitle">
            A privacy-conscious search engine built for the web.
          </p>

          <form className="search-form" onSubmit={handleSearch}>
            <div className="search-box">
              <span className="search-icon">⌕</span>

              <input
                type="text"
                placeholder="What do you want to search?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />

              {query && (
                <button
                  type="button"
                  className="clear-btn"
                  onClick={() => setQuery("")}
                >
                  ×
                </button>
              )}
            </div>

            <button type="submit" className="search-btn">
              Search
            </button>
          </form>

          <div className="privacy-note">
            <span>🔒</span>
            <span>No permanent search history</span>
            <span>•</span>
            <span>No user profiling</span>
          </div>
              {loading && (
  <div className="search-message">
    🔎 Searching...
  </div>
)}

{searchError && (
  <div className="search-error">
    ❌ {searchError}
  </div>
)}

{results.length > 0 && (
  <div className="results">
    <h2>Search Results</h2>

    {results.map((result, index) => (
      <article className="result-card" key={index}>
        <a
          href={result.url}
          target="_blank"
          rel="noopener noreferrer"
          className="result-title"
        >
          {result.title}
        </a>

        <div className="result-url">{result.url}</div>

        <p>{result.description}</p>
      </article>
    ))}
  </div>
)}
          {backendStatus && (
            <div className="backend-status">
              🟢 {backendStatus}
            </div>
          )}
        </div>
      </main>

      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">🔐</div>
          <h3>Privacy by Design</h3>
          <p>
            Minimal data collection with no permanent search-history profiles.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🧠</div>
          <h3>Semantic Search</h3>
          <p>
            Find relevant information based on meaning, not just exact words.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">⚡</div>
          <h3>Hybrid Ranking</h3>
          <p>
            Combine keyword and semantic retrieval for better results.
          </p>
        </div>
      </section>

      <footer className="footer">
        <span>PrivySearch</span>
        <span>Privacy-conscious search • Built as a learning project</span>
      </footer>
    </div>
  );
}

export default App;