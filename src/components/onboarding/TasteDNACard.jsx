import { ArrowRight, Share2 } from 'lucide-react';

const TasteDNACard = ({ tasteDNA, onContinue }) => {
  const handleShare = () => {
    const text = `My Taste DNA: ${tasteDNA.archetype}\nMusic: ${tasteDNA.music}\nMovies: ${tasteDNA.movies}\nBooks: ${tasteDNA.books}`;
    
    if (navigator.share) {
      navigator.share({ text });
    } else {
      navigator.clipboard.writeText(text);
      alert('Copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-2xl">
        {/* Title */}
        <div className="text-center mb-12">
          <h1 className="text-28 font-medium tracking-tighter text-foreground mb-3">
            Your Taste DNA
          </h1>
          <p className="text-13 text-muted-foreground">
            Here's what makes your feed unique
          </p>
        </div>

        {/* DNA Card */}
        <div className="bg-surface/50 border border-white/10 rounded-lg p-8 mb-8">
          {/* Archetype */}
          <div className="mb-8 pb-8 border-b border-white/10">
            <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
              Archetype
            </span>
            <h2 className="text-18 text-foreground font-medium mt-2">
              {tasteDNA.archetype}
            </h2>
          </div>

          {/* Interests */}
          <div className="space-y-6">
            {tasteDNA.music !== 'Not specified' && (
              <div>
                <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
                  Music
                </span>
                <p className="text-13 text-foreground mt-1">
                  {tasteDNA.music}
                </p>
              </div>
            )}

            {tasteDNA.movies !== 'Not specified' && (
              <div>
                <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
                  Movies
                </span>
                <p className="text-13 text-foreground mt-1">
                  {tasteDNA.movies}
                </p>
              </div>
            )}

            {tasteDNA.books !== 'Not specified' && (
              <div>
                <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
                  Books
                </span>
                <p className="text-13 text-foreground mt-1">
                  {tasteDNA.books}
                </p>
              </div>
            )}

            {tasteDNA.art !== 'Not specified' && (
              <div>
                <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
                  Art
                </span>
                <p className="text-13 text-foreground mt-1">
                  {tasteDNA.art}
                </p>
              </div>
            )}

            {tasteDNA.podcasts !== 'Not specified' && (
              <div>
                <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
                  Podcasts
                </span>
                <p className="text-13 text-foreground mt-1">
                  {tasteDNA.podcasts}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={handleShare}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-13 font-medium bg-surface/50 border border-white/10 text-foreground hover:bg-surface/80 hover:border-white/20 hover:-translate-y-0.5 transition-all duration-180 ease-out"
          >
            <Share2 className="w-4 h-4" strokeWidth={2} />
            Share
          </button>

          <button
            onClick={onContinue}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-13 font-medium bg-white text-black hover:bg-white/90 hover:-translate-y-0.5 transition-all duration-180 ease-out"
          >
            Continue to Feed
            <ArrowRight className="w-4 h-4" strokeWidth={2} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TasteDNACard;
