import SectionHeader from './SectionHeader';
import MediaCard from './MediaCard';

const FeedSection = ({ title, items }) => {
  return (
    <section className="mb-16">
      <SectionHeader title={title} count={items.length} />
      
      <div className="masonry-grid">
        {items.map((item) => (
          <MediaCard
            key={item.id}
            height={item.height}
            title={item.title}
            tag={item.tag}
            metadata={item.metadata}
          />
        ))}
      </div>
    </section>
  );
};

export default FeedSection;
