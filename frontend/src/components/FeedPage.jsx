import FeedSection from './FeedSection';

// Mock data generator
const generateMockItems = (category, count) => {
  const heights = ['small', 'medium', 'large', 'xlarge'];
  const tags = {
    music: ['Jazz', 'Electronic', 'Rock', 'Classical', 'Hip Hop', 'Indie'],
    movies: ['Drama', 'Sci-Fi', 'Thriller', 'Comedy', 'Documentary', 'Noir'],
    art: ['Abstract', 'Contemporary', 'Minimalism', 'Street Art', 'Digital', 'Photography'],
    fashion: ['Streetwear', 'Haute Couture', 'Vintage', 'Minimalist', 'Avant-Garde', 'Casual'],
    books: ['Fiction', 'Poetry', 'Philosophy', 'Biography', 'Essays', 'Classics'],
  };

  return Array.from({ length: count }, (_, i) => ({
    id: `${category}-${i}`,
    height: heights[Math.floor(Math.random() * heights.length)],
    tag: tags[category][Math.floor(Math.random() * tags[category].length)],
    title: `${category} Item ${i + 1}`,
    metadata: true,
  }));
};

const FeedPage = () => {
  const sections = [
    { title: 'Music', items: generateMockItems('music', 12) },
    { title: 'Movies', items: generateMockItems('movies', 10) },
    { title: 'Art', items: generateMockItems('art', 14) },
    { title: 'Fashion', items: generateMockItems('fashion', 8) },
    { title: 'Books', items: generateMockItems('books', 9) },
  ];

  return (
    <div className="min-h-screen">
      {/* Page Header */}
      <header className="sticky top-0 z-10 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="px-8 py-6">
          <h1 className="text-3xl font-normal font-display text-foreground">
            Your Feed
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Discover and explore cultural moments
          </p>
        </div>
      </header>

      {/* Feed Content */}
      <div className="px-8 py-8">
        {sections.map((section) => (
          <FeedSection
            key={section.title}
            title={section.title}
            items={section.items}
          />
        ))}
      </div>
    </div>
  );
};

export default FeedPage;
