import { ArrowRight, Share2, Headphones, Film, BookOpen, Image, Mic } from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from 'recharts';

const categoryConfig = {
  music: { 
    icon: Headphones, 
    color: 'hsl(270 50% 50%)',
    label: 'Music'
  },
  movies: { 
    icon: Film, 
    color: 'hsl(0 50% 50%)',
    label: 'Movies'
  },
  books: { 
    icon: BookOpen, 
    color: 'hsl(220 60% 45%)',
    label: 'Books'
  },
  art: { 
    icon: Image, 
    color: 'hsl(160 50% 45%)',
    label: 'Art'
  },
  podcasts: { 
    icon: Mic, 
    color: 'hsl(40 60% 50%)',
    label: 'Podcasts'
  }
};

const archetypeDescriptions = {
  'The Minimalist': 'Clean taste. Thoughtful content. You prefer focused, high-signal media.',
  'The Omnivore': 'Diverse interests. Broad curiosity. You consume content across all spectrums.',
  'The Creative': 'Artistic vision. Design-driven. You seek inspiration and creative expression.',
  'The Intellectual': 'Deep thinker. Knowledge seeker. You value substance and insight.',
  'The Explorer': 'Curious mind. Open to discovery. You embrace new experiences and perspectives.'
};

const TasteDNACard = ({ tasteDNA, onContinue, answers = {} }) => {
  const handleShare = () => {
    const text = `My Taste DNA: ${tasteDNA.archetype}\nMusic: ${tasteDNA.music}\nMovies: ${tasteDNA.movies}\nBooks: ${tasteDNA.books}`;
    
    if (navigator.share) {
      navigator.share({ text });
    } else {
      navigator.clipboard.writeText(text);
      alert('Copied to clipboard!');
    }
  };

  // Calculate raw scores from answer counts
  const rawScores = {
    music: answers.music?.length || 0,
    movies: answers.movies?.length || 0,
    books: answers.books?.length || 0,
    art: answers.art?.length || 0,
    podcasts: answers.podcasts?.length || 0
  };

  // Find maximum score for normalization
  const maxScore = Math.max(...Object.values(rawScores), 1); // Minimum 1 to avoid division by zero

  // Normalize scores to 0-10 scale
  const normalizedScores = Object.fromEntries(
    Object.entries(rawScores).map(([key, value]) => [
      key,
      Math.round((value / maxScore) * 10)
    ])
  );

  // Calculate radar chart data with normalized scores
  const radarData = [
    { category: 'Music', value: normalizedScores.music },
    { category: 'Movies', value: normalizedScores.movies },
    { category: 'Books', value: normalizedScores.books },
    { category: 'Art', value: normalizedScores.art },
    { category: 'Podcasts', value: normalizedScores.podcasts }
  ];

  // Get top preference per category
  const getTopPreference = (category) => {
    const items = answers[category];
    return items && items.length > 0 ? items[0] : 'Not specified';
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 py-12">
      <div 
        className="w-full max-w-3xl animate-in"
        style={{
          animation: 'fadeInUp 200ms ease-out',
        }}
      >
        <style>{`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(8px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}</style>

        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-28 font-medium tracking-tighter text-foreground mb-2">
            Your Taste DNA
          </h1>
          <p className="text-13 text-muted-foreground">
            A visual snapshot of your content identity
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-surface/50 border border-white/10 rounded-lg p-8 space-y-8">
          
          {/* 1. Archetype Hero Section */}
          <div className="text-center pb-8 border-b border-white/10">
            <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
              Archetype
            </span>
            <h2 className="text-28 font-medium tracking-tight text-foreground mt-2 mb-3">
              {tasteDNA.archetype}
            </h2>
            <p className="text-13 text-muted-foreground max-w-md mx-auto">
              {archetypeDescriptions[tasteDNA.archetype] || 'Your unique content personality.'}
            </p>
          </div>

          {/* 2. Category Grid with Icons */}
          <div className="grid grid-cols-2 gap-6">
            {Object.entries(categoryConfig).map(([key, config]) => {
              const Icon = config.icon;
              const preference = getTopPreference(key);
              
              return (
                <div key={key} className="flex items-center gap-3">
                  <Icon className="w-4 h-4 text-muted-foreground flex-shrink-0" strokeWidth={1.5} />
                  <div 
                    className="w-2 h-2 rounded-full flex-shrink-0" 
                    style={{ backgroundColor: config.color }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="text-11 text-muted-foreground uppercase tracking-wide">
                      {config.label}
                    </div>
                    <div className="text-13 text-foreground truncate">
                      {preference}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* 3. Radar Chart */}
          <div className="py-4">
            <div className="text-center mb-4">
              <span className="text-11 text-muted-foreground uppercase tracking-wide font-medium">
                Taste Map
              </span>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis 
                  dataKey="category" 
                  tick={{ fill: 'hsl(0 0% 55%)', fontSize: 12, fontFamily: 'IBM Plex Mono' }}
                />
                <Radar 
                  dataKey="value" 
                  stroke="rgba(255,255,255,0.8)" 
                  fill="rgba(255,255,255,0.15)" 
                  fillOpacity={1}
                  strokeWidth={2}
                  domain={[0, 10]}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* 4. Horizontal Taste Bars */}
          <div className="space-y-3">
            {Object.entries(categoryConfig).map(([key, config]) => {
              const score = normalizedScores[key];
              const percentage = score * 10; // Convert 0-10 scale to 0-100%
              
              return (
                <div key={key}>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-11 text-muted-foreground uppercase tracking-wide">
                      {config.label}
                    </span>
                    <span className="text-11 text-muted-foreground font-mono">
                      {score}
                    </span>
                  </div>
                  <div className="h-1 rounded bg-white/10 overflow-hidden">
                    <div 
                      className="h-full rounded transition-all duration-500 ease-out"
                      style={{ 
                        width: `${percentage}%`,
                        backgroundColor: config.color
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 5. Action Buttons */}
        <div className="flex gap-3 mt-6">
          <button
            onClick={handleShare}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-13 font-medium bg-surface/50 border border-white/10 text-foreground hover:bg-surface/80 hover:border-white/20 hover:-translate-y-0.5 transition-all duration-180 ease-out"
          >
            <Share2 className="w-4 h-4" strokeWidth={2} />
            Share Taste DNA
          </button>

          <button
            onClick={onContinue}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-13 font-medium bg-white text-black hover:bg-white/90 hover:-translate-y-0.5 transition-all duration-180 ease-out"
          >
            Enter Feed
            <ArrowRight className="w-4 h-4" strokeWidth={2} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TasteDNACard;
