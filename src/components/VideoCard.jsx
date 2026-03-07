import { Play } from 'lucide-react';

const categoryColors = {
  Music: { bg: 'hsl(270 50% 50% / 0.1)', text: 'hsl(270 50% 50%)', border: 'hsl(270 50% 50% / 0.3)' },
  Book: { bg: 'hsl(220 60% 45% / 0.1)', text: 'hsl(220 60% 45%)', border: 'hsl(220 60% 45% / 0.3)' },
  Movie: { bg: 'hsl(0 50% 50% / 0.1)', text: 'hsl(0 50% 50%)', border: 'hsl(0 50% 50% / 0.3)' },
  Artwork: { bg: 'hsl(160 50% 45% / 0.1)', text: 'hsl(160 50% 45%)', border: 'hsl(160 50% 45% / 0.3)' },
  Podcast: { bg: 'hsl(40 60% 50% / 0.1)', text: 'hsl(40 60% 50%)', border: 'hsl(40 60% 50% / 0.3)' },
  Article: { bg: 'hsl(0 0% 40% / 0.1)', text: 'hsl(0 0% 40%)', border: 'hsl(0 0% 40% / 0.3)' },
};

const VideoCard = ({ title, category, image, source = "YouTube" }) => {
  const colors = categoryColors[category] || categoryColors.Article;

  return (
    <div className="group flex flex-col h-full bg-surface/50 border border-white/10 rounded-lg overflow-hidden transition-all duration-180 ease-out hover:bg-surface/80 hover:-translate-y-0.5 cursor-pointer">
      {/* Video Thumbnail - 9:16 vertical ratio */}
      <div className="relative overflow-hidden aspect-[9/16]">
        {image ? (
          <>
            <img 
              src={image} 
              alt={title}
              className="w-full h-full object-cover transition-transform duration-200 ease-out group-hover:scale-[1.02]"
              loading="lazy"
            />
            
            {/* Play Indicator */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="bg-black/40 rounded-full p-3 backdrop-blur-sm">
                <Play className="w-6 h-6 text-white/80 fill-white/80" strokeWidth={0} />
              </div>
            </div>

            {/* Video Badge */}
            <div className="absolute top-3 left-3">
              <div className="text-11 uppercase tracking-wide px-2 py-1 rounded border border-white/10 bg-black/50 backdrop-blur-sm text-white/80 font-medium">
                Video
              </div>
            </div>
          </>
        ) : (
          <div className="absolute inset-0 bg-surface" />
        )}
      </div>

      {/* Content */}
      <div className="p-6 space-y-3 flex-1 flex flex-col">
        {/* Title row with category label */}
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-16 font-normal text-foreground leading-tight tracking-tight line-clamp-2 flex-1">
            {title}
          </h3>
          
          {/* Category label */}
          <div 
            className="flex-shrink-0 px-2.5 py-1 rounded text-11 font-medium uppercase tracking-wide flex items-center"
            style={{ 
              backgroundColor: colors.bg,
              color: colors.text,
              border: `1px solid ${colors.border}`
            }}
          >
            {category}
          </div>
        </div>

        {/* Source link */}
        <a 
          href="#" 
          className="text-13 text-muted-foreground hover:text-foreground transition-colors duration-160 inline-block w-fit"
          onClick={(e) => e.preventDefault()}
        >
          {source}
        </a>
      </div>
    </div>
  );
};

export default VideoCard;
