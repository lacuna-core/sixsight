export default function Hero() {
  return (
    <section className="hero">
      <div className="container">
        <div className="hero-eyebrow">
          <span className="hero-eyebrow-dot" />
          Toronto Open Data
        </div>
        <h1 className="hero-title">
          When data is public,<br />
          <em>accountability follows.</em>
        </h1>
        <p className="hero-body">
          SixSight transforms City of Toronto open datasets into clear, measurable insights —
          surfacing the patterns behind infrastructure delays, service gaps, and civic performance
          that deserve public attention.
        </p>
        <div className="hero-meta">
          <a className="hero-meta-item" href="https://open.toronto.ca/" target="_blank" rel="noreferrer">City of Toronto Open Data</a>
          <span className="hero-meta-sep" />
          <a className="hero-meta-item" href="https://github.com/lacuna-core/sixsight" target="_blank" rel="noreferrer">Open source</a>
        </div>
      </div>
    </section>
  )
}
