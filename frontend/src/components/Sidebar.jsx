import { 
  Layers, 
  Compass, 
  Grid3x3, 
  Sparkles, 
  User,
  Settings
} from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { icon: Layers, label: 'Feed', active: true },
    { icon: Compass, label: 'Explore', active: false },
    { icon: Grid3x3, label: 'Moodboards', active: false },
    { icon: Sparkles, label: 'Vibes', active: false },
    { icon: User, label: 'Profile', active: false },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-border bg-card">
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="border-b border-border px-6 py-6">
          <h1 className="font-display text-2xl font-normal text-foreground">
            VibeGraph
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.label}
                className={`
                  flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium
                  transition-colors duration-150
                  ${
                    item.active
                      ? 'bg-secondary text-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                  }
                `}
              >
                <Icon className="h-5 w-5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-border px-3 py-4">
          <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground transition-colors duration-150 hover:bg-accent hover:text-foreground">
            <Settings className="h-5 w-5" />
            <span>Settings</span>
          </button>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
