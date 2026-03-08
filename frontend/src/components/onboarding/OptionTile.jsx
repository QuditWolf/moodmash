import { Check } from 'lucide-react';

const OptionTile = ({ label, selected, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`
        relative p-4 rounded-lg border transition-all duration-180 ease-out text-left
        ${selected 
          ? 'bg-surface/80 border-white/20' 
          : 'bg-surface/50 border-white/10 hover:bg-surface/80 hover:border-white/20 hover:-translate-y-0.5'
        }
      `}
    >
      <span className="text-13 text-foreground font-mono">
        {label}
      </span>
      
      {selected && (
        <div className="absolute top-2 right-2">
          <Check className="w-4 h-4 text-white/60" strokeWidth={2} />
        </div>
      )}
    </button>
  );
};

export default OptionTile;
