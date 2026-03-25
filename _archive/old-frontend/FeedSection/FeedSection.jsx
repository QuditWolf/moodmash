import { motion } from 'framer-motion';
import FeedCard from '../FeedCard/FeedCard';
import './FeedSection.css';

const FeedSection = ({ title, items }) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.4 }
    }
  };

  return (
    <section className="feed-section">
      <div className="feed-section-header">
        <h2>{title}</h2>
        <button className="feed-section-view-all">View All</button>
      </div>
      
      <motion.div 
        className="feed-section-grid"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {items.map((item) => (
          <motion.div key={item.id} variants={itemVariants}>
            <FeedCard 
              image={item.image}
              title={item.title}
              category={item.category}
            />
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
};

export default FeedSection;
