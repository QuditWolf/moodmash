import { useState } from 'react';
import { Search, Filter, Grid, List as ListIcon } from 'lucide-react';
import { Card, Button, Input, EmptyState } from '@components';
import './DiscoverList.css';

const DiscoverList = () => {
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');

  const items = [
    {
      id: 1,
      title: 'The Remains of the Day',
      category: 'Books',
      author: 'Kazuo Ishiguro',
      vibe: 'Melancholic elegance',
      image: '📚',
      score: 95,
    },
    {
      id: 2,
      title: 'Lost in Translation',
      category: 'Films',
      director: 'Sofia Coppola',
      vibe: 'Urban loneliness',
      image: '🎬',
      score: 92,
    },
    {
      id: 3,
      title: 'Clair de Lune',
      category: 'Music',
      artist: 'Debussy',
      vibe: 'Ethereal calm',
      image: '🎵',
      score: 89,
    },
    {
      id: 4,
      title: 'Minimalist Wardrobe',
      category: 'Fashion',
      brand: 'Curated Selection',
      vibe: 'Refined simplicity',
      image: '👔',
      score: 88,
    },
    {
      id: 5,
      title: 'Starry Night',
      category: 'Art',
      artist: 'Vincent van Gogh',
      vibe: 'Emotional turbulence',
      image: '🎨',
      score: 97,
    },
    {
      id: 6,
      title: 'Norwegian Wood',
      category: 'Books',
      author: 'Haruki Murakami',
      vibe: 'Nostalgic melancholy',
      image: '📖',
      score: 94,
    },
  ];

  const filteredItems = items.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="discover-list-page">
      <div className="discover-header">
        <div>
          <h1>Discover</h1>
          <p className="discover-subtitle">Curated recommendations based on your taste graph</p>
        </div>
      </div>

      <div className="discover-toolbar">
        <div className="discover-search">
          <Input
            type="text"
            placeholder="Search across all categories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            leftIcon={<Search size={18} />}
          />
        </div>

        <div className="discover-actions">
          <Button variant="outline" leftIcon={<Filter size={18} />}>
            Filter
          </Button>
          
          <div className="view-toggle">
            <button
              className={`view-toggle-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
            >
              <Grid size={18} />
            </button>
            <button
              className={`view-toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
            >
              <ListIcon size={18} />
            </button>
          </div>
        </div>
      </div>

      {filteredItems.length > 0 ? (
        <div className={`discover-items ${viewMode}-view`}>
          {filteredItems.map((item) => (
            <Card key={item.id} variant="elevated" hoverable>
              <div className={`discover-item ${viewMode}-item`}>
                <div className="discover-item-icon">{item.image}</div>
                
                <div className="discover-item-content">
                  <div className="discover-item-header">
                    <span className="discover-item-category">{item.category}</span>
                    <span className="discover-item-score">{item.score}% match</span>
                  </div>
                  
                  <h3 className="discover-item-title">{item.title}</h3>
                  
                  <p className="discover-item-creator">
                    {item.author || item.director || item.artist || item.brand}
                  </p>
                  
                  <span className="discover-item-vibe">{item.vibe}</span>
                </div>

                <div className="discover-item-actions">
                  <Button variant="primary" size="sm">Save</Button>
                  <Button variant="outline" size="sm">Details</Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          icon={<Search size={48} />}
          title="No results found"
          description="Try adjusting your search or filters"
        />
      )}
    </div>
  );
};

export default DiscoverList;
