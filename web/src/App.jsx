import Header from './components/Header'
import Hero from './components/Hero'
import SubwayDelays from './components/SubwayDelays'
import Footer from './components/Footer'

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <SubwayDelays />
      </main>
      <Footer />
    </>
  )
}
