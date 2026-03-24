import { useState } from "react";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const metrics = [
  { value: "94%", label: "prediction response success" },
  { value: "<2s", label: "typical local feedback loop" },
  { value: "24/7", label: "ready for demo walkthroughs" },
];

const initialForm = {
  name: "",
  age: "",
  bp: "",
  sugar: "",
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${apiBaseUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name.trim(),
          age: Number(form.age),
          bp: Number(form.bp),
          sugar: Number(form.sugar),
        }),
      });

      if (!response.ok) {
        throw new Error("The backend rejected the request. Please check your API server.");
      }

      const data = await response.json();
      setResult(data);
    } catch (submitError) {
      setError(submitError.message || "Something went wrong while contacting the backend.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleReset() {
    setForm(initialForm);
    setResult(null);
    setError("");
  }

  const riskTone =
    result?.risk_level === "HIGH RISK" ? "risk-card high-risk" : "risk-card low-risk";
  const blockchainStatus = result?.blockchain;

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">Digital triage interface</p>
          <h1>PulseChain Health Risk Console</h1>
          <p className="hero-text">
            A polished patient intake screen for your healthcare workflow. Capture vitals,
            trigger the FastAPI prediction engine, and get a result panel that is ready for
            blockchain-backed record storage next.
          </p>

          <div className="metric-grid">
            {metrics.map((metric) => (
              <article className="metric-card" key={metric.label}>
                <strong>{metric.value}</strong>
                <span>{metric.label}</span>
              </article>
            ))}
          </div>
        </div>

        <div className="status-orbit" aria-hidden="true">
          <div className="orbit-ring orbit-ring-one"></div>
          <div className="orbit-ring orbit-ring-two"></div>
          <div className="pulse-core">
            <span>Live Data</span>
          </div>
        </div>
      </section>

      <section className="workspace-grid">
        <article className="panel glass-panel">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Patient intake</p>
              <h2>Run a risk prediction</h2>
            </div>
            <span className="panel-tag">FastAPI connected</span>
          </div>

          <form className="patient-form" onSubmit={handleSubmit}>
            <label>
              Patient name
              <input
                name="name"
                type="text"
                placeholder="Aarav Sharma"
                value={form.name}
                onChange={handleChange}
                required
              />
            </label>

            <div className="input-grid">
              <label>
                Age
                <input
                  name="age"
                  type="number"
                  min="0"
                  placeholder="52"
                  value={form.age}
                  onChange={handleChange}
                  required
                />
              </label>

              <label>
                Blood pressure
                <input
                  name="bp"
                  type="number"
                  min="0"
                  placeholder="138"
                  value={form.bp}
                  onChange={handleChange}
                  required
                />
              </label>

              <label>
                Sugar level
                <input
                  name="sugar"
                  type="number"
                  min="0"
                  placeholder="148"
                  value={form.sugar}
                  onChange={handleChange}
                  required
                />
              </label>
            </div>

            <div className="form-actions">
              <button className="primary-button" type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Analyzing..." : "Predict risk"}
              </button>
              <button className="secondary-button" type="button" onClick={handleReset}>
                Reset
              </button>
            </div>
          </form>

          {error ? <p className="error-banner">{error}</p> : null}
        </article>

        <article className="panel result-panel">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Prediction output</p>
              <h2>Clinical summary</h2>
            </div>
            <span className="panel-tag muted">Ready for chain logging</span>
          </div>

          {result ? (
            <div className={riskTone}>
              <p className="result-name">{result.name}</p>
              <h3>{result.risk_level}</h3>
              <p className="result-copy">
                {result.risk_level === "HIGH RISK"
                  ? "This patient should be prioritized for further review and recorded as a high-attention case."
                  : "Current indicators suggest a lower immediate risk profile, with routine follow-up still recommended."}
              </p>
              <div className="chain-status">
                <p>
                  Blockchain: <strong>{blockchainStatus?.status || "unknown"}</strong>
                </p>
                <p>{blockchainStatus?.message}</p>
                {blockchainStatus?.transaction_hash ? (
                  <p className="tx-hash">Tx: {blockchainStatus.transaction_hash}</p>
                ) : null}
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <p className="empty-badge">Awaiting submission</p>
              <h3>No prediction yet</h3>
              <p>
                Fill in the patient details and trigger the prediction engine to render the live risk
                assessment here.
              </p>
            </div>
          )}

          <div className="pipeline-card">
            <p className="pipeline-label">System pipeline</p>
            <div className="pipeline-flow">
              <span>Frontend</span>
              <span>Backend</span>
              <span>Prediction</span>
              <span>Blockchain</span>
            </div>
          </div>
        </article>
      </section>
    </main>
  );
}

export default App;
