import { 
  Layers, 
  Compass, 
  Grid3x3, 
  Sparkles, 
  User,
  Settings
} from 'lucide-react';
import { Button } from './ui/button';
import { Separator } from './ui/separator';

const Sidebar = () => {
  const navItems = [
    { icon: Layers, label: 'Feed', active: true },
    { icon: Compass, label: 'Explore', active: false },
    { icon: Grid3x3, label: 'Moodboards', active: false },
    { icon: Sparkles, label: 'Vibes', active: false },
    { icon: User, label: 'Profile', active: false },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-border bg-background">
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="flex h-16 items-center px-6">
          <span className="text-16 font-medium tracking-tight text-foreground">
            VibeGraph
          </span>
        </div>

        <Separator />

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-3 py-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Button
                key={item.label}
                variant="ghost"
                className={`
                  relative w-full justify-start gap-3 px-3 h-10 text-14 font-normal
                  transition-all duration-180 ease-premium
                  ${item.active 
                    ? 'accent-bar bg-surface text-foreground' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-surface/50'
                  }
                `}
              >
                <Icon className="h-4 w-4 icon-hover" strokeWidth={1.5} />
                <span className="tracking-tight">{item.label}</span>
              </Button>
            );
          })}
        </nav>

        <Separator />

        {/* Footer */}
        <div className="space-y-1 px-3 py-4">
          <Button
            variant="ghost"
            className="w-full justify-start gap-3 px-3 h-10 text-14 font-normal text-muted-foreground hover:text-foreground hover:bg-surface/50 transition-all duration-180 ease-premium"
          >
            <Settings className="h-4 w-4 icon-hover" strokeWidth={1.5} />
            <span className="tracking-tight">Settings</span>
          </Button>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
