const MediaCard = ({ height = 'medium', title, tag, metadata }) => {
  // Different height variants for masonry effect
  const heightClasses = {
    small: 'h-48',
    medium: 'h-64',
    large: 'h-80',
    xlarge: 'h-96',
  };

  return (
    <div className="masonry-grid-item group cursor-pointer">
      <div className="overflow-hidden rounded-lg border border-border bg-card shadow-sm transition-all duration-200 hover:shadow-md hover:border-foreground/20">
        {/* Placeholder Image Area */}
        <div className={`${heightClasses[height]} w-full bg-gradient-to-br from-foreground/90 to-foreground/70 relative overflow-hidden`}>
          {/* Skeleton shimmer effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-background/20 to-transparent animate-shimmer" />
          
          {/* Optional overlay on hover */}
          <div className="absolute inset-0 bg-background/0 group-hover:bg-background/10 transition-colors duration-200" />
        </div>

        {/* Card Content */}
        <div className="p-4 space-y-2">
          {/* Tag */}
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-muted-foreground">
              {tag}
            </span>
          </div>

          {/* Title Placeholder */}
          <div className="space-y-2">
            <div className="h-4 w-3/4 rounded bg-foreground/20 animate-pulse" />
            <div className="h-3 w-1/2 rounded bg-foreground/15 animate-pulse" />
          </div>

          {/* Metadata Placeholder */}
          {metadata && (
            <div className="flex items-center gap-2 pt-2">
              <div className="h-2 w-16 rounded bg-foreground/10 animate-pulse" />
              <div className="h-2 w-2 rounded-full bg-foreground/10" />
              <div className="h-2 w-12 rounded bg-foreground/10 animate-pulse" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MediaCard;
