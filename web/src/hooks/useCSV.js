import { useState, useEffect } from 'react'
import Papa from 'papaparse'

export function useCSV(path) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(path)
      .then(r => { if (!r.ok) throw new Error(r.statusText); return r.text() })
      .then(text => {
        const { data } = Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
        })
        setData(data)
        setLoading(false)
      })
      .catch(err => { setError(err); setLoading(false) })
  }, [path])

  return { data, loading, error }
}
