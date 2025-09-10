import './scrollbar.css'
import React, { useEffect, useMemo, useRef, useState } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const btnBase = {
  border: '1px solid rgba(255,255,255,0.06)',
  background: '#1f2937',
  color: '#e5e7eb',
  borderRadius: 12,
  fontSize: 18,
  padding: '14px 0',
  cursor: 'pointer',
  userSelect: 'none'
}
const variants = {
  light: {},
  accent: { background: '#2563eb', color: '#fff', border: '1px solid transparent' },
  danger: { background: '#b91c1c', color: '#fff', border: '1px solid transparent' },
}
function Button({ children, onClick, variant='light', span=1, disabled=false, title }) {
  return (
    <button
      type="button"
      title={title}
      onClick={onClick}
      disabled={disabled}
      style={{ ...btnBase, ...(variants[variant]||{}), gridColumn: `span ${span}`, opacity: disabled ? 0.6 : 1 }}
    >
      {children}
    </button>
  )
}

const isOp = (c) => ['+', '-', '*', '/', '^'].includes(c)

export default function App() {
  const [expr, setExpr] = useState('')
  const [screen, setScreen] = useState('0')
  const [items, setItems] = useState([])
  const [busy, setBusy] = useState(false)

  const displayRef = useRef(null)
  useEffect(() => {
    const el = displayRef.current
    if (el) el.scrollLeft = el.scrollWidth
  }, [screen])

  const normalized = useMemo(
    () => expr.replace(/×/g, '*').replace(/÷/g, '/').replace(/,/g, '.').replace(/\^/g, '**'),
    [expr]
  )

  async function fetchHistory() {
    try {
      const r = await fetch(`${API}/history`)
      const data = await r.json()
      setItems(Array.isArray(data) ? data : [])
    } catch {}
  }
  useEffect(() => { fetchHistory() }, [])

  useEffect(() => {
    const onKey = (e) => {
      const { key } = e
      if (/^\d$/.test(key)) return append(key)
      if (['+', '-', '*', '/', '(', ')', '.', ',', '^'].includes(key)) return append(key)
      if (key === '%') return percent()
      if (key === 'Enter' || key === '=') { e.preventDefault(); return calculate() }
      if (key === 'Backspace') return backspace()
      if (key === 'Escape') return clearAll()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  function setBoth(next) {
    setExpr(next)
    setScreen((next || '0').replace(/\./g, ','))
  }

  function lastNumberSpan(s) {
    const m = s.match(/(-?\d+(?:\.\d+)?)(?!.*-?\d+(?:\.\d+)?)/)
    if (!m) return null
    const end = m.index + m[0].length
    const start = m.index
    return { start, end, value: m[0] }
  }

  function replaceLastNumber(transform) {
    const span = lastNumberSpan(expr)
    if (!span) return
    const before = expr.slice(0, span.start)
    const after = expr.slice(span.end)
    const nextNum = transform(span.value)
    setBoth(before + nextNum + after)
  }

  function append(chRaw) {
    const map = { ',': '.', '×': '*', '÷': '/' }
    const ch = map[chRaw] ?? chRaw

    setExpr(prev => {
      let next = prev

      if (isOp(ch)) {
        if (!next) return '' 
        const last = next[next.length - 1]
        if (isOp(last)) next = next.slice(0, -1) 
      }

      if (ch === '.') {
        const span = lastNumberSpan(next)
        if (span && span.value.includes('.')) {
          setScreen((next || '0').replace(/\./g, ','))
          return next
        }
      }

      next = (next + ch).replace(/[^\d+\-*/().,^ ]/g, '')
      setScreen((next || '0').replace(/\./g, ','))
      return next
    })
  }

  function backspace() {
    setExpr(prev => {
      const next = prev.slice(0, -1)
      setScreen((next || '0').replace(/\./g, ','))
      return next
    })
  }

  function clearAll() { setBoth('') }
  function clearEntry() {
    const span = lastNumberSpan(expr)
    if (!span) return setBoth('')
    setBoth(expr.slice(0, span.start) + expr.slice(span.end))
  }
  function toggleSign() {
    const span = lastNumberSpan(expr)
    if (!span) return
    replaceLastNumber(num => (num.startsWith('-') ? num.slice(1) : '-' + num))
  }

  function percent() { replaceLastNumber(num => `(${num})/100`) }
  function reciprocal() { replaceLastNumber(num => `1/(${num})`) }
  function square() { replaceLastNumber(num => `(${num})^2`) }
  function sqrt() { replaceLastNumber(num => `(${num})^(1/2)`) }

  async function calculate() {
    if (!expr.trim() || busy) return
    setBusy(true)
    try {
      const r = await fetch(`${API}/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: normalized })
      })
      if (!r.ok) { setScreen('Ошибка'); return }
      const data = await r.json()
      const res = String(data.result ?? '')
      setBoth(res)
      fetchHistory()
    } finally {
      setBusy(false)
    }
  }

  function useFromHistory(row, e) {
    if (e && e.shiftKey) return setBoth(String(row.expression ?? ''))
    return setBoth(String(row.result ?? ''))
  }

  return (
    <div style={{ minHeight: '100vh', background: '#0b1220', color: '#e6edf3', display: 'flex', alignItems: 'flex-start', justifyContent: 'center', padding: 24 }}>
      <div style={{ width: 360 }}>
        <h1 style={{ fontSize: 20, fontWeight: 600, margin: '8px 0 12px' }}>Калькулятор</h1>

        {/* Экран с горизонтальным скроллом */}
        <div
          ref={displayRef}
          className="scrollx"
          style={{
            background: '#0f172a',
            border: '1px solid #23324d',
            borderRadius: 16,
            padding: '12px 12px',
            marginBottom: 10,
            textAlign: 'right',
            minHeight: 48,
            fontSize: 34,
            fontWeight: 500,
            overflowX: 'auto',
            whiteSpace: 'nowrap'
          }}
          title={screen}
        >
          {screen}
        </div>

        {/* Клавиатура (Windows layout) */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8 }}>
          <Button onClick={percent}>%</Button>
          <Button onClick={clearEntry}>CE</Button>
          <Button onClick={clearAll}>C</Button>
          <Button onClick={backspace} title="Backspace">⌫</Button>

          <Button onClick={reciprocal}>1/x</Button>
          <Button onClick={square}>x²</Button>
          <Button onClick={sqrt}>√x</Button>
          <Button onClick={() => append('÷')}>÷</Button>

          <Button onClick={() => append('7')}>7</Button>
          <Button onClick={() => append('8')}>8</Button>
          <Button onClick={() => append('9')}>9</Button>
          <Button onClick={() => append('×')}>×</Button>

          <Button onClick={() => append('4')}>4</Button>
          <Button onClick={() => append('5')}>5</Button>
          <Button onClick={() => append('6')}>6</Button>
          <Button onClick={() => append('-')}>−</Button>

          <Button onClick={() => append('1')}>1</Button>
          <Button onClick={() => append('2')}>2</Button>
          <Button onClick={() => append('3')}>3</Button>
          <Button onClick={() => append('+')}>+</Button>

          <Button onClick={toggleSign}>+/−</Button>
          <Button onClick={() => append('0')}>0</Button>
          <Button onClick={() => append(',')}>,</Button>
          <Button onClick={calculate} variant="accent" title="Enter" disabled={busy}>=</Button>
        </div>

        {/* История — строка скроллится целиком, даблклик вставляет результат */}
        <div style={{ marginTop: 18, border: '1px solid #23324d', borderRadius: 16, padding: 14 }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 8 }}>
            <h2 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>История</h2>
            <button
              type="button"
              onClick={async () => { if (busy) return; setBusy(true); try { await fetch(`${API}/delete/all`, { method:'DELETE' }) } finally { setBusy(false); fetchHistory() } }}
              style={{ ...btnBase, ...variants.danger, padding:'6px 10px', fontSize: 12 }}
              disabled={busy}
            >
              Очистить
            </button>
          </div>
          {items.length === 0 ? (
            <div style={{ opacity: 0.5 }}>Журнала ещё нет.</div>
          ) : (
            <ul style={{ listStyle: 'none', margin: 0, padding: 0, display:'flex', flexDirection:'column', gap: 6 }}>
              {items.map(row => (
                <li
                  key={row.id}
                  className="scrollx"
                  onDoubleClick={(e) => useFromHistory(row, e)}
                  style={{
                    cursor:'pointer',
                    overflowX:'auto',
                    whiteSpace:'nowrap',
                    padding: '6px 6px',
                    borderBottom:'1px solid #1e293b'
                  }}
                  title="Двойной клик — вставить результат. Shift+двойной — вставить выражение."
                >
                  <span style={{ opacity: 0.85 }}>{row.expression}</span>
                  <strong style={{ padding: '0 10px' }}>=</strong>
                  <span style={{ fontWeight: 700 }}>{row.result}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div style={{ marginTop: 14, opacity: 0.6, fontSize: 12 }}>API: {API}</div>
      </div>
    </div>
  )
}
