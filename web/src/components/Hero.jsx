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
          <span className="hero-meta-item">City of Toronto Open Data</span>
          <span className="hero-meta-sep" />
          <span className="hero-meta-item">Updated via TTC open data portal</span>
          <span className="hero-meta-sep" />
          <span className="hero-meta-item">Open source</span>
        </div>
      </div>
    </section>
  )
}
