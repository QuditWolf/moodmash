import { motion } from 'framer-motion';
import './FeedCard.css';

const FeedCard = ({ image, title, category }) => {
  return (
    <motion.div 
      className="feed-card"
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ duration: 0.3 }}
    >
      <div className="feed-card-image">
        <img src={image} alt={title} loading="lazy" />
      </div>
      <div className="feed-card-content">
        <span className="feed-card-category">{category}</span>
        <h3 className="feed-card-title">{title}</h3>
      </div>
    </motion.div>
  );
};

export default FeedCard;
