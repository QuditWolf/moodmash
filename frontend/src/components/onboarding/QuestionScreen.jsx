import OptionTile from './OptionTile';
import ProgressBar from './ProgressBar';
import { ArrowRight } from 'lucide-react';

const QuestionScreen = ({ 
  question, 
  currentIndex, 
  totalQuestions, 
  selectedOptions, 
  onToggleOption, 
  onNext,
  loading = false
}) => {
  const canProceed = selectedOptions.length > 0 && !loading;

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-4xl">
        {/* Progress */}
        <div className="mb-12">
          <ProgressBar current={currentIndex + 1} total={totalQuestions} />
        </div>

        {/* Question Title */}
        <h1 className="text-28 font-medium tracking-tighter text-foreground mb-8">
          {question.title}
        </h1>

        {/* Options Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-12">
          {question.options.map((option) => (
            <OptionTile
              key={option}
              label={option}
              selected={selectedOptions.includes(option)}
              onClick={() => onToggleOption(option)}
            />
          ))}
        </div>

        {/* Next Button */}
        <div className="flex justify-end">
          <button
            onClick={onNext}
            disabled={!canProceed}
            className={`
              flex items-center gap-2 px-6 py-3 rounded-lg text-13 font-medium
              transition-all duration-180 ease-out
              ${canProceed
                ? 'bg-white text-black hover:bg-white/90 hover:-translate-y-0.5'
                : 'bg-surface/50 text-muted-foreground cursor-not-allowed'
              }
            `}
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                Loading...
              </>
            ) : (
              <>
                {currentIndex === totalQuestions - 1 ? 'Finish' : 'Next'}
                <ArrowRight className="w-4 h-4" strokeWidth={2} />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuestionScreen;
