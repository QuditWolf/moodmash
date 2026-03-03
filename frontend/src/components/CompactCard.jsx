const categoryColors = {
  Music: { bg: 'hsl(270 50% 50% / 0.1)', text: 'hsl(270 50% 50%)', border: 'hsl(270 50% 50% / 0.3)' },
  Book: { bg: 'hsl(220 60% 45% / 0.1)', text: 'hsl(220 60% 45%)', border: 'hsl(220 60% 45% / 0.3)' },
  Movie: { bg: 'hsl(0 50% 50% / 0.1)', text: 'hsl(0 50% 50%)', border: 'hsl(0 50% 50% / 0.3)' },
  Artwork: { bg: 'hsl(160 50% 45% / 0.1)', text: 'hsl(160 50% 45%)', border: 'hsl(160 50% 45% / 0.3)' },
  Podcast: { bg: 'hsl(40 60% 50% / 0.1)', text: 'hsl(40 60% 50%)', border: 'hsl(40 60% 50% / 0.3)' },
  Article: { bg: 'hsl(0 0% 40% / 0.1)', text: 'hsl(0 0% 40%)', border: 'hsl(0 0% 40% / 0.3)' },
};

const CompactCard = ({ title, category, image, source = "Unsplash" }) => {
  const colors = categoryColors[category] || categoryColors.Article;

  return (
    <div className="flex gap-4 p-4 border border-white/10 rounded-lg bg-surface/50 hover:bg-surface/80 transition-all duration-180 cursor-pointer">
      {/* Thumbnail */}
      <div className="flex-shrink-0">
        {image ? (
          <img 
            src={image} 
            alt={title}
            className="w-20 h-24 object-cover rounded-md"
            loading="lazy"
          />
        ) : (
          <div className="w-20 h-24 bg-surface rounded-md" />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 flex flex-col justify-between min-w-0">
        <div>
          <h3 className="text-14 font-normal text-foreground leading-tight tracking-tight line-clamp-2 mb-1">
            {title}
          </h3>
          <p className="text-11 text-muted-foreground">
            {source}
          </p>
        </div>

        {/* Category label */}
        <div className="flex items-center">
          <div 
            className="px-2 py-0.5 rounded text-11 font-medium uppercase tracking-wide inline-block"
            style={{ 
              backgroundColor: colors.bg,
              color: colors.text,
              border: `1px solid ${colors.border}`
            }}
          >
            {category}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompactCard;
