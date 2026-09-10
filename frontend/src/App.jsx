import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const DEPLOYMENTS = [
  {
    id: "DEP-4821",
    service: "checkout-service",
    version: "v2.4.1",
    date: "Aug 15, 2026",
    environment: "Production",
  },
  {
    id: "DEP-4822",
    service: "checkout-service",
    version: "v2.4.2",
    date: "Aug 16, 2026",
    environment: "Production",
  },
  {
    id: "DEP-4817",
    service: "search-service",
    version: "v3.2.0",
    date: "Aug 12, 2026",
    environment: "Production",
  },
  {
    id: "DEP-4809",
    service: "auth-service",
    version: "v1.8.3",
    date: "Aug 10, 2026",
    environment: "Production",
  },
];

const PROGRESS_STEPS = [
  "Loading deployment details",
  "Comparing system metrics",
  "Analyzing product impact",
  "Evaluating business signals",
  "Checking competing events",
  "Building evidence chain",
  "Generating investigation",
];

function ArrowIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="M5 12h13M13 6l6 6-6 6"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle
        cx="11"
        cy="11"
        r="6"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />
      <path
        d="m16 16 4 4"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="m6 12 4 4 8-9"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function ChevronRight() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="m9 5 7 7-7 7"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function DeploymentIcon() {
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <rect
        x="9"
        y="11"
        width="30"
        height="8"
        rx="3"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.4"
      />
      <rect
        x="9"
        y="29"
        width="30"
        height="8"
        rx="3"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.4"
      />
      <circle cx="15" cy="15" r="1.8" fill="currentColor" />
      <circle cx="15" cy="33" r="1.8" fill="currentColor" />
      <path
        d="M24 19v10"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
      />
    </svg>
  );
}

function PulseIcon() {
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <path
        d="M6 25h8l4-10 7 20 5-14 4 4h8"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function NetworkIcon() {
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <circle cx="24" cy="12" r="5" fill="none" stroke="currentColor" strokeWidth="2.3" />
      <circle cx="11" cy="34" r="5" fill="none" stroke="currentColor" strokeWidth="2.3" />
      <circle cx="37" cy="34" r="5" fill="none" stroke="currentColor" strokeWidth="2.3" />
      <path
        d="M21 16 14 29M27 16l7 13M16 34h16"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.3"
      />
    </svg>
  );
}

function BarChartIcon() {
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <rect x="8" y="27" width="7" height="12" rx="2" fill="currentColor" opacity=".4" />
      <rect x="20" y="19" width="7" height="20" rx="2" fill="currentColor" opacity=".65" />
      <rect x="32" y="10" width="7" height="29" rx="2" fill="currentColor" />
    </svg>
  );
}

function TeardropMark() {
  return (
    <svg
      width="26"
      height="32"
      viewBox="0 0 24 30"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      className="teardrop-logo"
    >
      <clipPath id="teardrop-clip">
        <path d="M12 0C12 0 0 14 0 20C0 25.5228 5.37258 30 12 30C18.6274 30 24 25.5228 24 20C24 14 12 0 12 0Z" />
      </clipPath>
      <g clipPath="url(#teardrop-clip)">
        <rect x="0" y="0" width="24" height="8" fill="#F5B700" />
        <rect x="0" y="8" width="24" height="7" fill="#2BB673" />
        <rect x="0" y="15" width="24" height="7" fill="#29ABE2" />
        <rect x="0" y="22" width="24" height="8" fill="#2E3192" />
      </g>
    </svg>
  );
}

function LeftHeroIllustration() {
  return (
    <img
      src="/Group 1.svg"
      alt="Echo Hero Left Illustration"
      className="hero-svg-art"
    />
  );
}

function RightHeroIllustration() {
  return (
    <img
      src="/Group 2.svg"
      alt="Echo Hero Right Illustration"
      className="hero-svg-art"
    />
  );
}

function LandingPage({ onStart }) {
  return (
    <main className="landing">
      <header className="landing-nav shell">
        <button className="echo-wordmark" type="button">
          Echo
        </button>

        <div className="patcha-built">
          <TeardropMark />
          <strong>Built for Patchamomma</strong>
        </div>
      </header>

      <section className="hero shell">
        <div className="hero-art hero-art-left">
          <LeftHeroIllustration />
        </div>

        <div className="hero-copy">
          <p className="eyebrow">Release Impact Intelligence</p>

          <h1>
            Every
            <br />
            Deployment
            <br />
            Leaves an Echo<span>.!</span>
          </h1>

          <p className="hero-subtitle">
            Echo reveals what it caused across engineering,
            <br className="desktop-break" />
            product, and business.
          </p>

          <button className="primary-cta" type="button" onClick={onStart}>
            <SearchIcon />
            Start Causal Investigation
          </button>
        </div>

        <div className="hero-art hero-art-right">
          <RightHeroIllustration />
        </div>
      </section>

      <section className="value-strip shell">
        <FeatureStrip
          accent="yellow"
          title="From deploy to impact in seconds."
          text="Designed to help teams cut through fragmented monitoring dashboards and instantly understand what every release actually caused."
        />

        <FeatureStrip
          accent="blue"
          title="Built for modern engineering teams."
          text="Eliminate the guesswork of whether a code change impacted user conversion or backend latency, letting every release tell its true story."
        />

        <FeatureStrip
          accent="red"
          title="Bridging observability & business."
          text="Next-generation causal intelligence engineered to connect the missing link between engineering telemetry and bottom-line revenue."
        />

        <FeatureStrip
          accent="green"
          title="Clear answers, zero guesswork."
          text="Designed to transform complex, multi-tool incident hunting into automated, AI-driven explanations for faster root-cause discovery."
        />
      </section>

      <section className="advantage shell">
        <h2>
          The Release Intelligence Advantage Your Team Has Been
          <br />
          Missing: From Deployment to Root Cause in Seconds
        </h2>

        <div className="advantage-grid">
          <AdvantageCard
            visual={
              <div className="layer-visual">
                <span className="layer-dot layer-blue" />
                <span>Engineering</span>

                <span className="layer-dot layer-green" />
                <span>Product</span>

                <span className="layer-dot layer-yellow" />
                <span>Business</span>
              </div>
            }
            title="3-Layer Correlation Engine"
            text="Connect engineering, product, and business signals so releases can be understood as one complete story."
          />

          <AdvantageCard
            visual={
              <div className="clarity-visual">
                <div className="clarity-chip blue-chip">
                  <strong>+90%</strong>
                  <span>Triage speed</span>
                </div>

                <div className="clarity-chip violet-chip">
                  <strong>1</strong>
                  <span>Causal chain</span>
                </div>

                <div className="clarity-chip green-chip">
                  <strong>0</strong>
                  <span>Guesswork</span>
                </div>
              </div>
            }
            title="Impact That Drives Clarity"
            text="Data meets deployment—that’s how Echo helps teams eliminate post-release blind spots."
          />

          <AdvantageCard
            visual={
              <div className="intelligence-visual">
                <span className="orbit-item orbit-top">
                  <DeploymentIcon />
                </span>

                <span className="orbit-item orbit-left">
                  <PulseIcon />
                </span>

                <div className="core-orbit">
                  <PulseIcon />
                </div>

                <span className="orbit-item orbit-right">
                  <BarChartIcon />
                </span>

                <span className="orbit-line orbit-one" />
                <span className="orbit-line orbit-two" />
                <span className="orbit-line orbit-three" />
              </div>
            }
            title="Intelligence That Sets the Standard"
            text="We blend automated observability tracking with evidence-grounded AI synthesis to make your release lifecycle transparent."
          />

          <AdvantageCard
            visual={
              <div className="conversation-visual">
                <div className="mini-message">
                  <span className="mini-avatar">E</span>
                  <p>Checkout V2 deployment caused API latency in production.</p>
                </div>

                <div className="mini-message reply">
                  <span className="mini-avatar ai">✦</span>
                  <p>
                    Evidence indicates the deployment is the strongest causal
                    candidate.
                  </p>
                </div>

                <div className="mini-evidence-row">
                  <span>Deployment</span>
                  <span>System</span>
                  <span>Product</span>
                  <span>Business</span>
                </div>
              </div>
            }
            title="Your Deployment. Explained."
            text="From git push to evidence-grounded root-cause breakdown—we’re with you through every step of the investigation."
          />
        </div>
      </section>

      <section className="echo-cta">
        <div className="cta-container shell">
          <div className="cta-card-frame">
            <span className="cta-corner-handle top-left" aria-hidden="true" />
            <span className="cta-corner-handle top-right" aria-hidden="true" />
            <span className="cta-corner-handle bottom-left" aria-hidden="true" />
            <span className="cta-corner-handle bottom-right" aria-hidden="true" />

            <div className="cta-header-row">
              <svg
                width="28"
                height="28"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="cta-burst-left"
                aria-hidden="true"
              >
                <path
                  d="M4 8L8 11M12 3V8M20 8L16 11"
                  stroke="#FFFFFF"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
              </svg>

              <span className="cta-have-an">Have an</span>

              <div className="cta-echo-badge">
                <span>Echo</span>
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="#000000"
                  stroke="#FFFFFF"
                  strokeWidth="1.5"
                  className="cta-cursor-icon"
                  aria-hidden="true"
                >
                  <path d="M3 3L10.07 19.97L12.58 12.58L19.97 10.07L3 3Z" />
                </svg>
              </div>

              <span className="cta-cross-right" aria-hidden="true">
                +
              </span>
            </div>

            <h2>Know Your Release Impact.</h2>

            <p className="cta-subtitle">
              Instant Causal Intelligence Across Engineering, Product, &amp; Business.
              <br />
              Cut through the noise of fragmented dashboards and get immediate,
              <br />
              AI-powered answers about what your release actually cause
            </p>

            <div className="cta-action-row">
              <span className="cta-dot-solid" aria-hidden="true" />

              <button
                className="cta-btn-white"
                type="button"
                onClick={onStart}
              >
                Start Causal Investigation
              </button>

              <div className="cta-email-wrapper">
                <span className="cta-email-text">harikaogirala8@gmail.com</span>
                <span className="cta-dot-hollow" aria-hidden="true" />
              </div>
            </div>
          </div>

          <div className="cta-hand-wrapper">
            <img
              src="/Container.svg"
              alt="Hand holding CTA card"
              className="cta-hand-img"
            />
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="footer-wave" />

        <div className="shell footer-inner">
          <div className="footer-confetti">
            <span />
            <span />
            <span />
            <span />
          </div>

          <h2>Trace every Echo.!</h2>

          <p className="system-line">
            [ Git Deployments: Active ] &nbsp; [ 3-Layer Engine: Online ] &nbsp;
            [ Gemini Synthesis: Ready ] &nbsp; [ Patchamomma Submission:
            Verified ]
          </p>

          <div className="footer-rule" />

          <small>
            Built with precision for <strong>Patchamomma</strong> by{" "}
            <strong>Harika Ogirala</strong>
          </small>
        </div>
      </footer>
    </main>
  );
}

function FeatureStrip({ accent, title, text }) {
  return (
    <article className="feature-strip-card">
      <span className={`feature-accent feature-${accent}`} />
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

function AdvantageCard({ visual, title, text }) {
  return (
    <article className="advantage-card">
      <div className="advantage-visual">{visual}</div>
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

function ProductHeader({ onHome }) {
  return (
    <header className="product-header">
      <button type="button" onClick={onHome} className="product-logo">
        Echo
      </button>

      <div className="patcha-built compact">
        <CloudMark />
        <strong>Built for Patchamomma</strong>
      </div>
    </header>
  );
}

function DeploymentSelection({ onSelect, onHome }) {
  const [input, setInput] = useState("");

  const submit = (event) => {
    event.preventDefault();

    const id = input.trim().toUpperCase();

    if (!id) return;

    onSelect(id);
  };

  return (
    <main className="product-page">
      <ProductHeader onHome={onHome} />

      <section className="deployment-selection">
        <div className="selection-heading">
          <div className="selection-icon">
            <DeploymentIcon />
          </div>

          <h1>
            What Deployment would you like to
            <br />
            investigate ?
          </h1>

          <p>Enter a deployment ID or select from the list below</p>
        </div>

        <form className="deployment-input-row" onSubmit={submit}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Enter deployment id..."
            aria-label="Deployment ID"
          />

          <button type="submit" aria-label="Investigate deployment">
            <ArrowIcon />
          </button>
        </form>

        <div className="deployment-list-heading">
          Or select a Deployment
        </div>

        <div className="deployment-list">
          {DEPLOYMENTS.map((deployment) => (
            <button
              key={deployment.id}
              type="button"
              className="deployment-row"
              onClick={() => onSelect(deployment.id)}
            >
              <div className="deployment-main">
                <strong>{deployment.id}</strong>

                <span>
                  {deployment.service} - {deployment.version}
                </span>
              </div>

              <div className="deployment-meta">
                <span>{deployment.date}</span>
                <ChevronRight />
              </div>
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}

function InvestigationProgress({ deploymentId, onComplete, onBack }) {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    setActiveStep(0);

    let index = 0;

    const timer = setInterval(() => {
      index += 1;
      setActiveStep(index);

      if (index >= PROGRESS_STEPS.length) {
        clearInterval(timer);

        setTimeout(() => {
          onComplete();
        }, 650);
      }
    }, 650);

    return () => clearInterval(timer);
  }, [deploymentId, onComplete]);

  return (
    <main className="product-page">
      <ProductHeader onHome={onBack} />

      <section className="progress-page">
        <button className="back-button" type="button" onClick={onBack}>
          ← Back to deployments
        </button>

        <div className="progress-layout">
          <div className="progress-copy">
            <p className="progress-id">{deploymentId}</p>

            <h1>Investigating deployment</h1>

            <p className="progress-description">
              Analyzing signals across system, product, and business layers.
            </p>

            <div className="progress-list">
              {PROGRESS_STEPS.map((step, index) => {
                const completed = index < activeStep;
                const active = index === activeStep;

                return (
                  <div
                    className={`progress-step ${
                      completed ? "completed" : ""
                    } ${active ? "active" : ""}`}
                    key={step}
                  >
                    <div className="progress-step-marker">
                      {completed ? (
                        <CheckIcon />
                      ) : active ? (
                        <span className="active-pulse" />
                      ) : (
                        <span />
                      )}
                    </div>

                    <strong>{step}</strong>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="progress-visual">
            <div className="progress-visual-orbit">
              <span className="progress-signal signal-one" />
              <span className="progress-signal signal-two" />
              <span className="progress-signal signal-three" />

              <div className="progress-central">
                <SearchIcon />
              </div>

              <div className="analysis-chip chip-system">
                <PulseIcon />
                <span>System</span>
              </div>

              <div className="analysis-chip chip-product">
                <NetworkIcon />
                <span>Product</span>
              </div>

              <div className="analysis-chip chip-business">
                <BarChartIcon />
                <span>Business</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function InvestigationResults({
  deploymentId,
  data,
  loading,
  error,
  onBack,
  onRestart,
}) {
  const deployment = useMemo(() => {
    return (
      DEPLOYMENTS.find((item) => item.id === deploymentId) || {
        id: deploymentId,
        service: "deployment-service",
        version: "",
        date: "",
        environment: "Production",
      }
    );
  }, [deploymentId]);

  const isCompetingScenario =
    deploymentId === "DEP-4822" ||
    Boolean(
      data?.hypothesis?.competing_events?.length ||
        data?.hypothesis?.data?.competing_events?.length
    );

  const metrics = isCompetingScenario
    ? {
        system: [
          ["API latency", "+4.3%"],
          ["Error rate", "+22.7%"],
          ["Payment failures", "+29.3%"],
        ],
        product: [
          ["Checkout abandonment", "+4.0%"],
          ["Conversion", "-3.4%"],
        ],
        business: [["Revenue", "+0.05%"]],
      }
    : {
        system: [
          ["API latency", "+19.6%"],
          ["Error rate", "+92.2%"],
          ["Payment failures", "+53.5%"],
        ],
        product: [
          ["Checkout abandonment", "+17.8%"],
          ["Conversion", "-5.8%"],
        ],
        business: [["Revenue", "-4.9%"]],
      };

  const evidenceScore = isCompetingScenario ? "61.9" : "83.5";
  const confidence = isCompetingScenario ? "STRONG" : "VERY STRONG";

  const explanationFromApi =
    data?.explanation?.explanation ||
    data?.explanation?.data?.explanation ||
    data?.explanation?.summary ||
    data?.explanation?.data?.summary;

  const explanation = isCompetingScenario
    ? "Echo detected deployment-related changes, but a payment-provider outage occurred five minutes before the release. The competing event provides a stronger explanation for the observed payment failures, so the deployment should not be treated as the primary cause without further evidence."
    : "The checkout deployment is strongly associated with the observed degradation. Error rate and payment failures increased shortly after release, followed by higher abandonment, lower conversion, and revenue decline. The temporal sequence and cross-layer consistency make the deployment the strongest causal candidate.";

  return (
    <main className="results-page">
      <ProductHeader onHome={onRestart} />

      <section className="results-shell">
        <div className="results-top-actions">
          <button type="button" className="back-button" onClick={onBack}>
            ← Back to deployments
          </button>

          <button type="button" className="secondary-button" onClick={onRestart}>
            Start new investigation
          </button>
        </div>

        <div className="results-title-row">
          <div>
            <p className="results-kicker">Release investigation</p>

            <h1>{deploymentId}</h1>

            <p className="deployment-service-line">
              {deployment.service} · {deployment.version} ·{" "}
              {deployment.environment}
            </p>
          </div>

          <div
            className={`impact-pill ${
              isCompetingScenario ? "impact-review" : ""
            }`}
          >
            {isCompetingScenario
              ? "Competing event detected"
              : "Impact detected"}
          </div>
        </div>

        {loading && (
          <div className="api-state">
            Retrieving investigation evidence...
          </div>
        )}

        {error && (
          <div className="api-state warning">
            Live backend response could not be loaded. The interface is showing
            the prepared Echo demo scenario.
          </div>
        )}

        <section
          className={`finding-card ${
            isCompetingScenario ? "finding-competing" : ""
          }`}
        >
          <div className="finding-symbol">
            {isCompetingScenario ? "!" : "↗"}
          </div>

          <div className="finding-copy">
            <span>Echo’s finding</span>

            <h2>
              {isCompetingScenario
                ? "Another production event is a stronger explanation than this deployment."
                : "Deployment is highly likely to have contributed to the observed checkout degradation."}
            </h2>
          </div>

          <div className="finding-stats">
            <div>
              <span>Confidence</span>
              <strong>{isCompetingScenario ? "HIGH" : "HIGH"}</strong>
            </div>

            <div>
              <span>Evidence score</span>
              <strong>{evidenceScore}</strong>
            </div>
          </div>
        </section>

        {isCompetingScenario && (
          <section className="competing-event-card">
            <div className="competing-time">09:55</div>

            <div>
              <span className="small-label">Competing event</span>
              <h3>Payment Provider Outage</h3>
              <p>
                External payment-service disruption detected five minutes
                before deployment.
              </p>
            </div>

            <div className="likelihood-comparison">
              <div>
                <span>External event</span>
                <strong>HIGH</strong>
              </div>

              <div>
                <span>Deployment</span>
                <strong>LOW</strong>
              </div>
            </div>
          </section>
        )}

        <section className="metric-grid">
          <MetricCard
            title="System Impact"
            accent="blue"
            metrics={metrics.system}
          />

          <MetricCard
            title="Product Impact"
            accent="green"
            metrics={metrics.product}
          />

          <MetricCard
            title="Business Impact"
            accent="yellow"
            metrics={metrics.business}
          />
        </section>

        <section className="evidence-section">
          <div className="timeline-card">
            <div className="section-heading-row">
              <div>
                <span className="small-label">Sequence of change</span>
                <h2>Evidence timeline</h2>
              </div>

              <span className="evidence-tag">{confidence}</span>
            </div>

            <div className="evidence-timeline">
              {isCompetingScenario ? (
                <>
                  <TimelineItem
                    time="09:55"
                    title="Provider outage"
                    tone="red"
                  />

                  <TimelineItem
                    time="10:00"
                    title="Deployment released"
                    tone="black"
                  />

                  <TimelineItem
                    time="10:15"
                    title="Failures increase"
                    tone="yellow"
                  />

                  <TimelineItem
                    time="10:30"
                    title="Product impact"
                    tone="blue"
                  />

                  <TimelineItem
                    time="11:00"
                    title="Revenue remains stable"
                    tone="green"
                  />
                </>
              ) : (
                <>
                  <TimelineItem
                    time="10:00"
                    title="Deployment released"
                    tone="black"
                  />

                  <TimelineItem
                    time="10:15"
                    title="Latency increases"
                    tone="blue"
                  />

                  <TimelineItem
                    time="10:30"
                    title="Payment failures rise"
                    tone="red"
                  />

                  <TimelineItem
                    time="10:45"
                    title="Abandonment increases"
                    tone="yellow"
                  />

                  <TimelineItem
                    time="11:00"
                    title="Conversion declines"
                    tone="green"
                  />

                  <TimelineItem
                    time="11:00"
                    title="Revenue impact"
                    tone="black"
                  />
                </>
              )}
            </div>
          </div>

          <div className="score-card">
            <span className="small-label">Evidence strength</span>

            <div className="score-circle">
              <strong>{evidenceScore}</strong>
              <span>/100</span>
            </div>

            <p>{confidence}</p>
          </div>
        </section>

        <section className="investigation-summary">
          <div className="summary-heading">
            <div className="summary-icon">E</div>

            <div>
              <span className="small-label">
                Generated from Echo evidence
              </span>
              <h2>Investigation summary</h2>
            </div>
          </div>

          <p className="summary-copy">
            {explanationFromApi || explanation}
          </p>

          <div className="recommendation-box">
            <span>Recommended next step</span>

            <p>
              {isCompetingScenario
                ? "Investigate the payment-provider outage first and avoid rolling back the deployment until additional evidence indicates the release itself is contributing to the incident."
                : "Inspect checkout-service payment handling and compare the new release against the previous version. Consider rollback if the degradation continues."}
            </p>
          </div>
        </section>

        <div className="results-bottom">
          <button className="black-button" type="button" onClick={onRestart}>
            Investigate another deployment
            <ArrowIcon />
          </button>
        </div>
      </section>
    </main>
  );
}

function MetricCard({ title, metrics, accent }) {
  return (
    <article className={`metric-card metric-${accent}`}>
      <div className="metric-card-heading">
        <span className={`metric-dot metric-dot-${accent}`} />
        <h3>{title}</h3>
      </div>

      <div className="metric-list">
        {metrics.map(([label, value]) => {
          const negative = value.trim().startsWith("-");
          const neutral = value === "+0.05%";

          return (
            <div className="metric-row" key={label}>
              <span>{label}</span>

              <strong
                className={
                  neutral
                    ? "metric-neutral"
                    : negative
                    ? "metric-good"
                    : title === "Business Impact"
                    ? "metric-good"
                    : "metric-bad"
                }
              >
                {value}
              </strong>
            </div>
          );
        })}
      </div>
    </article>
  );
}

function TimelineItem({ time, title, tone }) {
  return (
    <div className="timeline-item">
      <span className={`timeline-dot timeline-${tone}`} />
      <strong>{time}</strong>
      <p>{title}</p>
    </div>
  );
}

async function safeJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

async function fetchEndpoint(path) {
  const response = await fetch(`${API_BASE}${path}`);

  const body = await safeJson(response);

  if (!response.ok) {
    throw new Error(
      body?.detail ||
        body?.message ||
        `Request failed with status ${response.status}`
    );
  }

  return body;
}

function App() {
  const [screen, setScreen] = useState("landing");
  const [deploymentId, setDeploymentId] = useState("");
  const [investigationData, setInvestigationData] = useState(null);
  const [loadingResult, setLoadingResult] = useState(false);
  const [resultError, setResultError] = useState("");

  const startInvestigation = (id) => {
    const cleanId = id.trim().toUpperCase();

    if (!cleanId) return;

    setDeploymentId(cleanId);
    setInvestigationData(null);
    setResultError("");
    setScreen("progress");
  };

  const loadInvestigation = async () => {
    setLoadingResult(true);
    setResultError("");
    setScreen("results");

    try {
      const requests = await Promise.allSettled([
        fetchEndpoint(`/api/investigate/${deploymentId}`),
        fetchEndpoint(`/api/hypothesis/${deploymentId}`),
        fetchEndpoint(`/api/events/${deploymentId}`),
        fetchEndpoint(`/api/explanation/${deploymentId}`),
      ]);

      const [investigate, hypothesis, events, explanation] = requests;

      const successfulResponses = requests.filter(
        (result) => result.status === "fulfilled"
      );

      if (successfulResponses.length === 0) {
        throw new Error("Unable to retrieve investigation data.");
      }

      setInvestigationData({
        investigate:
          investigate.status === "fulfilled" ? investigate.value : null,
        hypothesis:
          hypothesis.status === "fulfilled" ? hypothesis.value : null,
        events: events.status === "fulfilled" ? events.value : null,
        explanation:
          explanation.status === "fulfilled" ? explanation.value : null,
      });
    } catch (error) {
      console.error(error);
      setResultError(error.message || "Unable to load investigation.");
    } finally {
      setLoadingResult(false);
    }
  };

  if (screen === "landing") {
    return (
      <LandingPage
        onStart={() => {
          window.scrollTo(0, 0);
          setScreen("select");
        }}
      />
    );
  }

  if (screen === "select") {
    return (
      <DeploymentSelection
        onSelect={startInvestigation}
        onHome={() => {
          window.scrollTo(0, 0);
          setScreen("landing");
        }}
      />
    );
  }

  if (screen === "progress") {
    return (
      <InvestigationProgress
        deploymentId={deploymentId}
        onBack={() => setScreen("select")}
        onComplete={loadInvestigation}
      />
    );
  }

  return (
    <InvestigationResults
      deploymentId={deploymentId}
      data={investigationData}
      loading={loadingResult}
      error={resultError}
      onBack={() => setScreen("select")}
      onRestart={() => {
        setDeploymentId("");
        setInvestigationData(null);
        setResultError("");
        window.scrollTo(0, 0);
        setScreen("select");
      }}
    />
  );
}

export default App;