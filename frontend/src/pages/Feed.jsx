import { motion } from 'framer-motion';
import FeedSection from '../components/FeedSection/FeedSection';
import './Feed.css';

// Mock data for different sections
const mockData = {
  music: [
    {
      id: 1,
      image: 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=800',
      title: 'Midnight Jazz Sessions',
      category: 'Jazz',
    },
    {
      id: 2,
      image: 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800',
      title: 'Electronic Dreams',
      category: 'Electronic',
    },
    {
      id: 3,
      image: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800',
      title: 'Acoustic Vibes',
      category: 'Acoustic',
    },
    {
      id: 4,
      image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800',
      title: 'Indie Rock Essentials',
      category: 'Rock',
    },
  ],
  movies: [
    {
      id: 5,
      image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800',
      title: 'Cinematic Masterpieces',
      category: 'Drama',
    },
    {
      id: 6,
      image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800',
      title: 'Sci-Fi Classics',
      category: 'Sci-Fi',
    },
    {
      id: 7,
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800',
      title: 'Noir Collection',
      category: 'Noir',
    },
    {
      id: 8,
      image: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800',
      title: 'Indie Films',
      category: 'Indie',
    },
  ],
  art: [
    {
      id: 9,
      image: 'https://images.unsplash.com/photo-1547891654-e66ed7ebb968?w=800',
      title: 'Abstract Expressions',
      category: 'Abstract',
    },
    {
      id: 10,
      image: 'https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=800',
      title: 'Modern Minimalism',
      category: 'Minimalism',
    },
    {
      id: 11,
      image: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=800',
      title: 'Street Art Culture',
      category: 'Street Art',
    },
    {
      id: 12,
      image: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800',
      title: 'Contemporary Works',
      category: 'Contemporary',
    },
  ],
  books: [
    {
      id: 13,
      image: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800',
      title: 'Literary Fiction',
      category: 'Fiction',
    },
    {
      id: 14,
      image: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800',
      title: 'Poetry Collection',
      category: 'Poetry',
    },
    {
      id: 15,
      image: 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800',
      title: 'Philosophy Reads',
      category: 'Philosophy',
    },
  ],
};

const Feed = () => {
  return (
    <motion.div 
      className="feed-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      <div className="feed-header">
        <h1>Your Feed</h1>
        <p>Discover and explore cultural moments</p>
      </div>

      <div className="feed-content">
        <FeedSection 
          title="Music" 
          items={mockData.music}
        />
        
        <FeedSection 
          title="Movies" 
          items={mockData.movies}
        />
        
        <FeedSection 
          title="Art & Pictures" 
          items={mockData.art}
        />
        
        <FeedSection 
          title="Books" 
          items={mockData.books}
        />
      </div>
    </motion.div>
  );
};

export default Feed;
