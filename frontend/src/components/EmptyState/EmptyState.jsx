import Button from '../Button/Button';
import './EmptyState.css';

const EmptyState = ({
  icon,
  title,
  description,
  action,
  actionLabel,
  onAction,
}) => {
  return (
    <div className="empty-state">
      {icon && <div className="empty-state-icon">{icon}</div>}
      <h3 className="empty-state-title">{title}</h3>
      {description && <p className="empty-state-description">{description}</p>}
      {action && onAction && (
        <Button onClick={onAction} variant="primary">
          {actionLabel || action}
        </Button>
      )}
    </div>
  );
};

export default EmptyState;
