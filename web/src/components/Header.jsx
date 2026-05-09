export default function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="header-inner">
          <a href="/" className="wordmark">
            <span className="wordmark-six">Six</span>Sight
          </a>
          <nav className="nav">
            <a href="#subway-delays" className="nav-link active">Subway Delays</a>
          </nav>
        </div>
      </div>
    </header>
  )
}
