export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-inner">
          <p className="footer-copy">
            © {new Date().getFullYear()} SixSight &mdash; Data:{' '}
            <a href="https://open.toronto.ca" target="_blank" rel="noreferrer">
              City of Toronto Open Data
            </a>
          </p>
          <p className="footer-mission">
            Built to make civic data legible. If a city can be measured, it can be improved.
          </p>
        </div>
      </div>
    </footer>
  )
}
