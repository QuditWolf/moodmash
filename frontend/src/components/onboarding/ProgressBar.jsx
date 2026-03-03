const ProgressBar = ({ current, total }) => {
  const percentage = (current / total) * 100;

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-3">
        <span className="text-13 text-muted-foreground font-mono">
          Question {current} of {total}
        </span>
        <span className="text-13 text-muted-foreground font-mono">
          {Math.round(percentage)}%
        </span>
      </div>
      <div className="w-full h-1 bg-surface rounded-full overflow-hidden">
        <div 
          className="h-full bg-white/20 transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
