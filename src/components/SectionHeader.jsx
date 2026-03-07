import { Button } from './ui/button';

const SectionHeader = ({ title, count }) => {
  return (
    <div className="flex items-center justify-between mb-8 col-span-full">
      <div className="flex items-center gap-3">
        <h2 className="text-20 font-medium text-foreground tracking-tighter">
          {title}
        </h2>
        {count && (
          <span className="text-14 text-subtle-foreground font-mono">
            {count}
          </span>
        )}
      </div>
      <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
        View all
      </Button>
    </div>
  );
};

export default SectionHeader;
