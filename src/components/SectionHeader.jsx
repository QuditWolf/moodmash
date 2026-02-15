const SectionHeader = ({ title, count }) => {
  return (
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center gap-3">
        <h2 className="text-2xl font-normal font-display text-foreground">
          {title}
        </h2>
        {count && (
          <span className="inline-flex items-center rounded-full bg-muted px-3 py-1 text-xs font-medium text-muted-foreground">
            {count}
          </span>
        )}
      </div>
      <button className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
        View all
      </button>
    </div>
  );
};

export default SectionHeader;
