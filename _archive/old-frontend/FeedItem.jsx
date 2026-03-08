import MediaCard from './MediaCard';
import VideoCard from './VideoCard';

const FeedItem = ({ item, variant = 'normal' }) => {
  // Tall cards render as video cards
  if (variant === 'tall') {
    return (
      <div className="break-inside-avoid mb-6">
        <VideoCard {...item} />
      </div>
    );
  }

  // Adjust image aspect ratio for featured cards
  const imageAspectClass = variant === 'featured' ? 'aspect-[16/9]' : 'aspect-[4/5]';

  return (
    <div className="break-inside-avoid mb-6">
      <MediaCard
        {...item}
        imageAspect={imageAspectClass}
        isFeatured={variant === 'featured'}
      />
    </div>
  );
};

export default FeedItem;
