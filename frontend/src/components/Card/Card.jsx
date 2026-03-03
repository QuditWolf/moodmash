import { motion } from 'framer-motion';
import './Card.css';

const Card = ({
  children,
  variant = 'default',
  hoverable = false,
  className = '',
  onClick,
  ...props
}) => {
  const classes = [
    'card',
    `card-${variant}`,
    hoverable && 'card-hoverable',
    onClick && 'card-clickable',
    className,
  ].filter(Boolean).join(' ');

  const Component = hoverable || onClick ? motion.div : 'div';
  const motionProps = hoverable || onClick ? {
    whileHover: { y: -4, boxShadow: 'var(--shadow-xl)' },
    whileTap: onClick ? { scale: 0.98 } : {},
  } : {};

  return (
    <Component
      className={classes}
      onClick={onClick}
      {...motionProps}
      {...props}
    >
      {children}
    </Component>
  );
};

export default Card;
