import { NavLink } from 'react-router-dom'
import { Fingerprint, Route, BarChart3, Shield, Menu, X, Home } from 'lucide-react'
import { useState } from 'react'

const Sidebar = () => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const sessionId = sessionStorage.getItem('session_id')

  const navItems = [
    { icon: Home, label: 'Feed', to: `/feed` },
    { icon: Fingerprint, label: 'Taste DNA', to: `/dna/${sessionId}` },
    { icon: Route, label: 'Growth Path', to: `/path/${sessionId}` },
    { icon: BarChart3, label: 'Analytics', to: `/analytics/${sessionId}` },
    { icon: Shield, label: 'My Data', to: `/data/${sessionId}` },
  ]

  const navContent = (
    <div className="flex h-full flex-col">
      {/* Logo */}
      <div className="flex h-16 items-center justify-between px-6 border-b border-white/10">
        <span className="text-base font-medium tracking-tight text-foreground font-mono">
          MoodMash
        </span>
        <button
          onClick={() => setMobileOpen(false)}
          className="md:hidden text-muted-foreground hover:text-foreground"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-6">
        {navItems.map((item) => {
          const Icon = item.icon
          const disabled = item.label !== 'Feed' && !sessionId

          if (disabled) {
            return (
              <div
                key={item.label}
                className="flex items-center gap-3 px-3 h-10 rounded-lg text-sm font-mono text-muted-foreground/40 cursor-not-allowed w-full"
              >
                <Icon className="h-4 w-4 flex-shrink-0" strokeWidth={1.5} />
                <span className="tracking-tight">{item.label}</span>
              </div>
            )
          }

          return (
            <NavLink
              key={item.label}
              to={item.to}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 h-10 rounded-lg text-sm font-mono transition-all duration-180 w-full ${
                  isActive
                    ? 'text-foreground bg-white/5'
                    : 'text-muted-foreground hover:text-foreground hover:bg-white/5'
                }`
              }
            >
              <Icon className="h-4 w-4 flex-shrink-0" strokeWidth={1.5} />
              <span className="tracking-tight">{item.label}</span>
            </NavLink>
          )
        })}

        {!sessionId && (
          <NavLink
            to="/onboard"
            onClick={() => setMobileOpen(false)}
            className="flex items-center gap-3 px-3 h-10 rounded-lg text-sm font-mono text-muted-foreground hover:text-foreground hover:bg-white/5 transition-all duration-180 w-full mt-4"
          >
            <span className="tracking-tight">Start Onboarding</span>
          </NavLink>
        )}
      </nav>

      {/* Footer */}
      <div className="px-6 py-4 border-t border-white/10">
        <p className="text-xs text-muted-foreground/50 font-mono">
          Your data stays yours.
        </p>
      </div>
    </div>
  )

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setMobileOpen(true)}
        className="fixed top-4 left-4 z-50 md:hidden p-2 rounded-lg bg-background border border-white/10 text-foreground"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 md:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed left-0 top-0 h-screen w-64 border-r border-white/10 bg-black z-50
          transition-transform duration-200 ease-out
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
          md:translate-x-0
          hidden md:flex md:flex-col
          ${mobileOpen ? '!flex' : ''}
        `}
      >
        {navContent}
      </aside>
    </>
  )
}

export default Sidebar
