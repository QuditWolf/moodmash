import './Loader.css';

const Loader = ({ size = 'md', text, fullScreen = false }) => {
  const sizeClasses = {
    sm: 'loader-sm',
    md: 'loader-md',
    lg: 'loader-lg',
  };

  const content = (
    <div className="loader-content">
      <div className={`loader ${sizeClasses[size]}`}>
        <div className="loader-circle"></div>
        <div className="loader-circle"></div>
        <div className="loader-circle"></div>
      </div>
      {text && <p className="loader-text">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="loader-fullscreen">
        {content}
      </div>
    );
  }

  return content;
};

export default Loader;
