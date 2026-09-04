import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [backendStatus, setBackendStatus] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchError, setSearchError] = useState("");

  const [showPrivacy, setShowPrivacy] = useState(false);
  const [privacyData, setPrivacyData] = useState(null);

  const [showEvaluation, setShowEvaluation] = useState(false);
  const [evaluationData, setEvaluationData] = useState(null);

  // -----------------------------
  // Backend Health Check
  // -----------------------------

  const checkBackend = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/health"
      );

      if (!response.ok) {
        throw new Error("Health API request failed");
      }

      const data = await response.json();

      setBackendStatus(
        `${data.service} is ${data.status}`
      );
    } catch (error) {
      setBackendStatus("Backend connection failed");
      console.error(error);
    }
  };

  // -----------------------------
  // Load Privacy Information
  // -----------------------------

  const loadPrivacyData = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/privacy"
      );

      if (!response.ok) {
        throw new Error("Privacy API request failed");
      }

      const data = await response.json();

      setPrivacyData(data);
    } catch (error) {
      console.error("Privacy API error:", error);
    }
  };

  // -----------------------------
  // Load Evaluation Report
  // -----------------------------

  const loadEvaluationData = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/evaluation"
      );

      if (!response.ok) {
        throw new Error("Evaluation API request failed");
      }

      const data = await response.json();

      setEvaluationData(data);
    } catch (error) {
      console.error("Evaluation API error:", error);
    }
  };

  // -----------------------------
  // Search
  // -----------------------------

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    setLoading(true);
    setSearchError("");
    setResults([]);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/search?query=${encodeURIComponent(
          query
        )}`
      );

      if (!response.ok) {
        throw new Error("Search request failed");
      }

      const data = await response.json();

      setResults(data.results);
    } catch (error) {
      console.error(error);

      setSearchError(
        "Unable to connect to the search service."
      );
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Open Evaluation Dashboard
  // -----------------------------

  const openEvaluation = () => {
    setShowEvaluation(true);
    loadEvaluationData();
  };

  return (
    <div className="app">

      {/* ============================= */}
      {/* Header */}
      {/* ============================= */}

      <header className="header">

        <div className="logo">
          <span className="logo-icon">🔐</span>
          <span>PrivySearch</span>
        </div>

        <div className="header-actions">

          <button
            className="evaluation-btn"
            onClick={openEvaluation}
          >
            📊 Evaluation
          </button>

          <button
            className="privacy-btn"
            onClick={() => {
              setShowPrivacy(true);
              loadPrivacyData();
            }}
          >
            🛡️ Privacy Center
          </button>

        </div>

      </header>


      {/* ============================= */}
      {/* Privacy Center */}
      {/* ============================= */}

      {showPrivacy && (

        <div className="privacy-panel">

          <div className="privacy-panel-content">

            <div className="privacy-panel-header">

              <h2>🛡️ Privacy Center</h2>

              <button
                className="privacy-close"
                onClick={() => setShowPrivacy(false)}
              >
                ×
              </button>

            </div>


            <p className="privacy-intro">
              PrivySearch is designed to minimize
              unnecessary data collection while
              providing useful search results.
            </p>


            {/* Privacy data loaded from backend */}

            {privacyData ? (

              <div className="privacy-items">

                <div className="privacy-item">

                  <span>
                    {privacyData.search_history.stored
                      ? "⚠️"
                      : "✅"}
                  </span>

                  <div>

                    <strong>
                      No permanent search history
                    </strong>

                    <p>
                      {
                        privacyData.search_history
                          .description
                      }
                    </p>

                  </div>

                </div>


                <div className="privacy-item">

                  <span>
                    {privacyData.user_profiling.enabled
                      ? "⚠️"
                      : "✅"}
                  </span>

                  <div>

                    <strong>
                      No user profiling
                    </strong>

                    <p>
                      {
                        privacyData.user_profiling
                          .description
                      }
                    </p>

                  </div>

                </div>


                <div className="privacy-item">

                  <span>
                    {privacyData.tracking
                      .third_party_trackers
                      ? "⚠️"
                      : "✅"}
                  </span>

                  <div>

                    <strong>
                      No unnecessary tracking
                    </strong>

                    <p>
                      {
                        privacyData.tracking
                          .description
                      }
                    </p>

                  </div>

                </div>


                <div className="privacy-item">

                  <span>
                    {privacyData.privacy_by_design
                      ? "🔒"
                      : "⚠️"}
                  </span>

                  <div>

                    <strong>
                      Privacy by design
                    </strong>

                    <p>
                      Privacy controls are enforced
                      through the backend architecture.
                    </p>

                  </div>

                </div>


                <div className="privacy-item">

                  <span>
                    {privacyData.data_collection
                      .query_storage
                      ? "⚠️"
                      : "✅"}
                  </span>

                  <div>

                    <strong>
                      Query storage disabled
                    </strong>

                    <p>
                      Search queries are not stored
                      as permanent user data.
                    </p>

                  </div>

                </div>


                <div className="privacy-item">

                  <span>
                    {privacyData.data_collection
                      .user_identification
                      ? "⚠️"
                      : "✅"}
                  </span>

                  <div>

                    <strong>
                      No user identification
                    </strong>

                    <p>
                      The search system does not require
                      user identification for searching.
                    </p>

                  </div>

                </div>

              </div>

            ) : (

              <div className="search-message">
                🔒 Loading privacy information...
              </div>

            )}


            {/* Backend status */}

            <button
              className="privacy-api-check"
              onClick={checkBackend}
            >
              Check System Status
            </button>


            {backendStatus && (

              <div className="backend-status">
                🟢 {backendStatus}
              </div>

            )}

          </div>

        </div>

      )}


      {/* ============================= */}
      {/* Evaluation Dashboard */}
      {/* ============================= */}

      {showEvaluation && (

        <div className="evaluation-panel">

          <div className="evaluation-panel-content">

            <div className="evaluation-header">

              <div>
                <h2>📊 Search Evaluation</h2>

                <p>
                  Benchmark performance of the PrivySearch
                  retrieval system.
                </p>
              </div>

              <button
                className="privacy-close"
                onClick={() => setShowEvaluation(false)}
              >
                ×
              </button>

            </div>


            {evaluationData ? (

              <>

                {/* ============================= */}
                {/* Metric Cards */}
                {/* ============================= */}

                <div className="evaluation-metrics">

                  <div className="metric-card">

                    <span className="metric-icon">
                      🎯
                    </span>

                    <div>
                      <span className="metric-label">
                        Top-1 Accuracy
                      </span>

                      <strong>
                        {evaluationData.top1_accuracy}%
                      </strong>
                    </div>

                  </div>


                  <div className="metric-card">

                    <span className="metric-icon">
                      🏆
                    </span>

                    <div>
                      <span className="metric-label">
                        Top-3 Accuracy
                      </span>

                      <strong>
                        {evaluationData.top3_accuracy}%
                      </strong>
                    </div>

                  </div>


                  <div className="metric-card">

                    <span className="metric-icon">
                      ⚡
                    </span>

                    <div>
                      <span className="metric-label">
                        Average Latency
                      </span>

                      <strong>
                        {evaluationData.average_latency_ms} ms
                      </strong>
                    </div>

                  </div>


                  <div className="metric-card">

                    <span className="metric-icon">
                      📈
                    </span>

                    <div>
                      <span className="metric-label">
                        P50 Latency
                      </span>

                      <strong>
                        {evaluationData.p50_latency_ms} ms
                      </strong>
                    </div>

                  </div>


                  <div className="metric-card">

                    <span className="metric-icon">
                      🚀
                    </span>

                    <div>
                      <span className="metric-label">
                        P95 Latency
                      </span>

                      <strong>
                        {evaluationData.p95_latency_ms} ms
                      </strong>
                    </div>

                  </div>


                  <div className="metric-card">

                    <span className="metric-icon">
                      🔎
                    </span>

                    <div>
                      <span className="metric-label">
                        Benchmark Queries
                      </span>

                      <strong>
                        {evaluationData.total_queries}
                      </strong>
                    </div>

                  </div>

                </div>


                {/* ============================= */}
                {/* Benchmark Results */}
                {/* ============================= */}

                <div className="evaluation-results">

                  <h3>
                    Benchmark Query Results
                  </h3>

                  <div className="evaluation-table-wrapper">

                    <table className="evaluation-table">

                      <thead>

                        <tr>
                          <th>Query</th>
                          <th>Expected Result</th>
                          <th>Top Result</th>
                          <th>Top-1</th>
                          <th>Top-3</th>
                          <th>Latency</th>
                        </tr>

                      </thead>

                      <tbody>

                        {evaluationData.results.map(
                          (item, index) => (

                            <tr key={index}>

                              <td>
                                {item.query}
                              </td>

                              <td>
                                {item.expected}
                              </td>

                              <td>
                                {item.top_result}
                              </td>

                              <td>

                                <span
                                  className={
                                    item.top1
                                      ? "eval-pass"
                                      : "eval-fail"
                                  }
                                >
                                  {item.top1
                                    ? "✓ Pass"
                                    : "✗ Miss"}
                                </span>

                              </td>

                              <td>

                                <span
                                  className={
                                    item.top3
                                      ? "eval-pass"
                                      : "eval-fail"
                                  }
                                >
                                  {item.top3
                                    ? "✓ Pass"
                                    : "✗ Miss"}
                                </span>

                              </td>

                              <td>
                                {item.latency_ms} ms
                              </td>

                            </tr>

                          )
                        )}

                      </tbody>

                    </table>

                  </div>

                </div>


                {/* ============================= */}
                {/* Evaluation Summary */}
                {/* ============================= */}

                <div className="evaluation-summary">

                  <div className="summary-icon">
                    💡
                  </div>

                  <div>

                    <strong>
                      Evaluation Summary
                    </strong>

                    <p>
                      PrivySearch achieved{" "}
                      <b>
                        {evaluationData.top1_accuracy}%
                      </b>{" "}
                      Top-1 accuracy and{" "}
                      <b>
                        {evaluationData.top3_accuracy}%
                      </b>{" "}
                      Top-3 accuracy across{" "}
                      <b>
                        {evaluationData.total_queries}
                      </b>{" "}
                      benchmark queries.
                      Average search latency was{" "}
                      <b>
                        {evaluationData.average_latency_ms} ms
                      </b>.
                    </p>

                  </div>

                </div>

              </>

            ) : (

              <div className="search-message">
                📊 Loading evaluation report...
              </div>

            )}

          </div>

        </div>

      )}


      {/* ============================= */}
      {/* Main */}
      {/* ============================= */}

      <main className="main">

        <div className="hero">

          <div className="brand-icon">
            🔎
          </div>


          <h1>
            Search <span>without profiling.</span>
          </h1>


          <p className="subtitle">
            A privacy-conscious search engine built
            for the web.
          </p>


          {/* Search Form */}

          <form
            className="search-form"
            onSubmit={handleSearch}
          >

            <div className="search-box">

              <span className="search-icon">
                ⌕
              </span>


              <input
                type="text"
                placeholder="What do you want to search?"
                value={query}
                onChange={(e) =>
                  setQuery(e.target.value)
                }
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


            <button
              type="submit"
              className="search-btn"
              disabled={loading}
            >
              {loading
                ? "Searching..."
                : "Search"}
            </button>

          </form>


          {/* Privacy Note */}

          <div className="privacy-note">

            <span>🔒</span>

            <span>
              No permanent search history
            </span>

            <span>•</span>

            <span>
              No user profiling
            </span>

          </div>


          {/* Loading */}

          {loading && (

            <div className="search-message">
              🔎 Searching...
            </div>

          )}


          {/* Error */}

          {searchError && (

            <div className="search-error">
              ❌ {searchError}
            </div>

          )}


          {/* ============================= */}
          {/* Results */}
          {/* ============================= */}

          {results.length > 0 && (

            <div className="results">

              <h2>
                Search Results
              </h2>


              {results.map((result, index) => (

                <article
                  className="result-card"
                  key={`${result.url}-${index}`}
                >

                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="result-title"
                  >
                    {result.title}
                  </a>


                  <div className="result-url">
                    {result.url}
                  </div>


                  <p>
                    {result.description}
                  </p>


                  <div className="result-meta">

                    <span>
                      Relevance:{" "}
                      {Math.round(
                        (result.hybrid_score || 0) * 100
                      )}
                      %
                    </span>

                  </div>

                </article>

              ))}

            </div>

          )}

        </div>

      </main>


      {/* ============================= */}
      {/* Features */}
      {/* ============================= */}

      <section className="features">

        <div className="feature-card">

          <div className="feature-icon">
            🔐
          </div>

          <h3>
            Privacy by Design
          </h3>

          <p>
            Minimal data collection with no
            permanent search-history profiles.
          </p>

        </div>


        <div className="feature-card">

          <div className="feature-icon">
            🧠
          </div>

          <h3>
            Semantic Search
          </h3>

          <p>
            Find relevant information based on
            meaning, not just exact words.
          </p>

        </div>


        <div className="feature-card">

          <div className="feature-icon">
            ⚡
          </div>

          <h3>
            Hybrid Ranking
          </h3>

          <p>
            Combine keyword and semantic retrieval
            for better results.
          </p>

        </div>

      </section>


      {/* ============================= */}
      {/* Footer */}
      {/* ============================= */}

      <footer className="footer">

        <span>
          PrivySearch
        </span>

        <span>
          Privacy-conscious search • Built as
          a learning project
        </span>

      </footer>

    </div>
  );
}

export default App;