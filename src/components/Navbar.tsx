import { useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'

const links = [['teams', '#teams'], ['how it works', '#how-it-works'], ['specialists', '#specialists'], ['docs', '#docs']]

function AuraMark() {
  return <svg aria-hidden="true" viewBox="0 0 32 32" className="h-7 w-7 fill-[#1a1a1a]"><path d="M16 2c2.3 5.5 2.3 10.1 0 14 3.9-3 8.6-3.7 14-2.2-2.2 5.2-6 8-11.5 8.2 4.8 1.4 8.2 4.1 10.2 8C23.2 31.5 18.8 29.5 16 25c.2 5-1.8 8-6.2 9-1.8-4.5-1.3-8.2 1.5-11.1-4.5 2.8-8.2 2.4-11.3-.9 3.2-3.5 7-4.5 11.4-3C7.5 17 4.3 13.7 3 8.5c5.3-1.2 9.7.3 13 4.5C13.8 9 13.8 5.4 16 2Z"/></svg>
}

export function Navbar() {
  const [open, setOpen] = useState(false)
  return <header className="fixed top-0 left-0 w-full z-50 py-6 md:py-8 bg-gradient-to-b from-[#f1f1f1]/80 to-transparent backdrop-blur-[2px]"><div className="grid grid-cols-12 max-w-7xl mx-auto px-5 sm:px-8 items-center">
    <a href="#top" className="col-span-6 md:col-span-3 flex items-center gap-2"><AuraMark/><span className="text-[21px] sm:text-[26px] tracking-tight text-black font-medium select-none font-display">Aura.dev</span></a>
    <nav className="hidden md:flex md:col-span-6 justify-center text-sm text-black lowercase">{links.map(([name, href], index) => <span key={name}><a href={href} className="hover:opacity-60 transition-opacity">{name}</a>{index < links.length - 1 && <span className="opacity-40">,&nbsp;</span>}</span>)}</nav>
    <div className="col-span-6 md:col-span-3 flex justify-end items-center gap-4"><a href="#contact" className="hidden sm:block text-sm text-black hover:opacity-60 transition-opacity">talk to us</a><a href="#teams" className="hidden md:block rounded-full bg-black px-4 py-2 text-sm text-white">build your team →</a>
    <button aria-label="Toggle menu" onClick={() => setOpen(value => !value)} className="relative z-20 h-9 w-9 md:hidden">{[0, 1, 2].map(index => <span key={index} className={`absolute left-1.5 w-6 h-[2px] bg-black transition-all duration-300 ${open ? index === 0 ? 'rotate-45 translate-y-[7px]' : index === 1 ? 'opacity-0' : '-rotate-45 -translate-y-[7px]' : ''}`} style={{ top: `${10 + index * 7}px` }} />)}</button>
    </div></div><AnimatePresence>{open && <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -16 }} className="absolute top-full left-0 z-10 flex w-full flex-col gap-5 bg-white/95 px-8 py-8 backdrop-blur-sm md:hidden">{links.map(([name, href]) => <a onClick={() => setOpen(false)} href={href} key={name}>{name}</a>)}</motion.div>}</AnimatePresence>
  </header>
}
