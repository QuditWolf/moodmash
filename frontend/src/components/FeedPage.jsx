import MediaCard from './MediaCard';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Button } from './ui/button';
import { Search } from 'lucide-react';

// Curated aesthetic images from Unsplash
const imageCollections = {
  music: [
    'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800&q=80',
    'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=800&q=80',
    'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&q=80',
    'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800&q=80',
  ],
  movies: [
    'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=80',
    'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800&q=80',
    'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800&q=80',
    'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&q=80',
  ],
  art: [
    'https://images.unsplash.com/photo-1547891654-e66ed7ebb968?w=800&q=80',
    'https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=800&q=80',
    'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=800&q=80',
    'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800&q=80',
  ],
  books: [
    'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&q=80',
    'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
    'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&q=80',
    'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&q=80',
  ],
  podcasts: [
    'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=800&q=80',
    'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=80',
    'https://images.unsplash.com/photo-1589903308904-1010c2294adc?w=800&q=80',
    'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800&q=80',
  ],
  articles: [
    'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&q=80',
    'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&q=80',
    'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=800&q=80',
    'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&q=80',
  ],
};

const titles = {
  music: ['Midnight Jazz Sessions', 'Electronic Dreams', 'Acoustic Vibes', 'Indie Rock Essentials'],
  movies: ['Cinematic Masterpieces', 'Sci-Fi Classics', 'Noir Collection', 'Indie Films'],
  art: ['Abstract Expressions', 'Modern Minimalism', 'Street Art Culture', 'Contemporary Works'],
  books: ['Literary Fiction', 'Poetry Collection', 'Philosophy Reads', 'Classic Novels'],
  podcasts: ['Tech Talks', 'Design Thinking', 'Startup Stories', 'Creative Process'],
  articles: ['Product Strategy', 'Design Systems', 'Engineering Culture', 'Growth Tactics'],
};

// Generate unified mixed feed
const generateUnifiedFeed = (count) => {
  const categories = ['Music', 'Book', 'Movie', 'Artwork', 'Podcast', 'Article'];
  const categoryMap = {
    'Music': 'music',
    'Book': 'books',
    'Movie': 'movies',
    'Artwork': 'art',
    'Podcast': 'podcasts',
    'Article': 'articles',
  };
  
  const sources = ['Unsplash', 'Spotify', 'IMDb', 'Artsy', 'Apple', 'Medium'];

  return Array.from({ length: count }, (_, i) => {
    const category = categories[i % categories.length];
    const categoryKey = categoryMap[category];
    const images = imageCollections[categoryKey] || [];
    const itemTitles = titles[categoryKey] || [];

    return {
      id: `item-${i}`,
      category,
      title: itemTitles[i % itemTitles.length],
      image: images[i % images.length],
      source: sources[Math.floor(Math.random() * sources.length)],
    };
  });
};

const FeedPage = () => {
  const feedItems = generateUnifiedFeed(24);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-white/10 bg-background/95 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-6">
          <div className="flex h-16 items-center justify-between">
            <h1 className="text-28 font-medium tracking-tighter text-foreground">
              Feed
            </h1>
            
            <div className="flex items-center gap-4">
              <Button 
                variant="ghost" 
                size="icon"
                className="hover:bg-surface/50 transition-all duration-160"
              >
                <Search className="h-4 w-4" strokeWidth={1.5} />
              </Button>
              <Avatar className="hover:bg-surface/50 transition-all duration-160 cursor-pointer">
                <AvatarFallback>VG</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      {/* Feed Grid - Premium SaaS Layout */}
      <div className="py-6 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-12 gap-6">
            {feedItems.map((item) => (
              <div 
                key={item.id}
                className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3"
              >
                <MediaCard
                  image={item.image}
                  title={item.title}
                  category={item.category}
                  source={item.source}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeedPage;
