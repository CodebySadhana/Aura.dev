import { Navbar } from './components/Navbar'
import { Hero } from './components/Hero'
import { InquiryHero } from './components/InquiryHero'
import { OrgShowcase } from './components/OrgShowcase'
import { HowItWorks } from './components/HowItWorks'
import { DocsExperience } from './components/DocsExperience'

export default function App() {
  const [teamContext, setTeamContext] = useState('')
  return <div className="relative min-h-screen bg-bg-base selection:bg-brand-green selection:text-black font-sans antialiased overflow-x-hidden">
    <Navbar />
    <main><InquiryHero onDeploy={capabilities => setTeamContext(`Build an Aura.dev team for ${capabilities.join(', ')}. Define the plan, delegate work, and verify the result.`)} /><Hero taskContext={teamContext} /><OrgShowcase id="teams" mode="teams" /><HowItWorks /><OrgShowcase id="specialists" mode="specialists" /><DocsExperience /></main>
  </div>
}
import { useState } from 'react'
