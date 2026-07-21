import { useEffect, useState } from 'react'

export function useTypewriter(text: string, speed = 38, startDelay = 600) {
  const [displayed, setDisplayed] = useState('')
  const [reduced, setReduced] = useState(false)
  useEffect(() => {
    const media = matchMedia('(prefers-reduced-motion: reduce)')
    const update = () => setReduced(media.matches)
    update(); media.addEventListener('change', update)
    return () => media.removeEventListener('change', update)
  }, [])
  useEffect(() => {
    if (reduced) { setDisplayed(text); return }
    setDisplayed('')
    let interval: ReturnType<typeof setInterval>
    const delay = setTimeout(() => { let index = 0; interval = setInterval(() => { setDisplayed(text.slice(0, ++index)); if (index === text.length) clearInterval(interval) }, speed) }, startDelay)
    return () => { clearTimeout(delay); clearInterval(interval) }
  }, [text, speed, startDelay, reduced])
  return { displayed, done: displayed.length === text.length, reduced }
}
