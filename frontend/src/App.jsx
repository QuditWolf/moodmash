import { BrowserRouter, Routes, Route, Outlet, Navigate } from 'react-router-dom'
import Landing from './pages/Landing'
import Feed from './pages/Feed'
import OnboardingPage from './components/Onboarding/OnboardingPage'
import DNACard from './components/DNACard/DNACard'
import GrowthPath from './components/GrowthPath/GrowthPath'
import Analytics from './components/Analytics/Analytics'
import DataPanel from './components/DataPanel/DataPanel'
import Sidebar from './components/common/Sidebar'
import NotFound from './pages/NotFound'

function AppLayout() {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <main className="flex-1 ml-0 md:ml-64">
        <Outlet />
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/onboard" element={<OnboardingPage />} />
        <Route element={<AppLayout />}>
          <Route path="/feed" element={<Feed />} />
          <Route path="/dna/:id" element={<DNACard />} />
          <Route path="/path/:id" element={<GrowthPath />} />
          <Route path="/analytics/:id" element={<Analytics />} />
          <Route path="/data/:id" element={<DataPanel />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
