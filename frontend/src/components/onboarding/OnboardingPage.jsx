import { useState, useEffect } from 'react';
import QuestionScreen from './QuestionScreen';
import TasteDNACard from './TasteDNACard';
import { vibeGraphAPI } from '../../services/vibeGraphAPI';

const OnboardingPage = ({ onComplete }) => {
  // Phase state: 'section1' | 'section2' | 'processing' | 'complete'
  const [phase, setPhase] = useState('section1');
  const [sessionId, setSessionId] = useState(null);
  
  // Questions state
  const [section1Questions, setSection1Questions] = useState([]);
  const [section2Questions, setSection2Questions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  
  // Answers state
  const [section1Answers, setSection1Answers] = useState([]);
  const [section2Answers, setSection2Answers] = useState([]);
  
  // Results state
  const [tasteDNA, setTasteDNA] = useState(null);
  
  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get current questions based on phase
  const currentQuestions = phase === 'section1' ? section1Questions : section2Questions;
  const currentQuestion = currentQuestions[currentQuestionIndex];
  
  // Get current answers based on phase
  const currentAnswers = phase === 'section1' ? section1Answers : section2Answers;
  const currentAnswer = currentAnswers.find(a => a.questionId === currentQuestion?.id);
  const selectedOptions = currentAnswer?.selectedOptions || [];

  // Load Section 1 questions on mount
  useEffect(() => {
    const loadSection1 = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await vibeGraphAPI.quiz.startSection1();
        setSessionId(response.sessionId);
        setSection1Questions(response.questions);
      } catch (err) {
        setError(err.message || 'Failed to load questions. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    loadSection1();
  }, []);

  const handleToggleOption = (option) => {
    const updateAnswers = phase === 'section1' ? setSection1Answers : setSection2Answers;
    
    updateAnswers(prev => {
      const existingAnswer = prev.find(a => a.questionId === currentQuestion.id);
      
      if (existingAnswer) {
        // Update existing answer
        const isSelected = existingAnswer.selectedOptions.includes(option);
        return prev.map(a => 
          a.questionId === currentQuestion.id
            ? {
                ...a,
                selectedOptions: isSelected
                  ? a.selectedOptions.filter(o => o !== option)
                  : [...a.selectedOptions, option]
              }
            : a
        );
      } else {
        // Create new answer
        return [...prev, {
          questionId: currentQuestion.id,
          selectedOptions: [option]
        }];
      }
    });
  };

  const handleNext = async () => {
    const isLastQuestion = currentQuestionIndex === currentQuestions.length - 1;
    
    if (isLastQuestion) {
      if (phase === 'section1') {
        // Completed Section 1 - load Section 2
        await loadSection2();
      } else if (phase === 'section2') {
        // Completed Section 2 - complete quiz
        await completeQuiz();
      }
    } else {
      // Move to next question
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const loadSection2 = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await vibeGraphAPI.quiz.generateSection2(sessionId, section1Answers);
      setSection2Questions(response.questions);
      setPhase('section2');
      setCurrentQuestionIndex(0);
    } catch (err) {
      setError(err.message || 'Failed to load next section. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const completeQuiz = async () => {
    setPhase('processing');
    setLoading(true);
    setError(null);
    
    try {
      // Get userId from localStorage or generate temporary one
      const userId = localStorage.getItem('userId') || `temp-${Date.now()}`;
      
      const allAnswers = {
        section1: section1Answers,
        section2: section2Answers
      };
      
      const response = await vibeGraphAPI.quiz.completeQuiz(sessionId, userId, allAnswers);
      setTasteDNA(response.tasteDNA);
      setPhase('complete');
      
      // Store in localStorage
      localStorage.setItem('taste_profile', JSON.stringify({
        userId,
        tasteDNA: response.tasteDNA,
        embeddingId: response.embeddingId,
        completedAt: new Date().toISOString()
      }));
    } catch (err) {
      setError(err.message || 'Failed to complete quiz. Please try again.');
      setPhase('section2'); // Return to section2 on error
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    
    if (phase === 'section1' && section1Questions.length === 0) {
      // Retry loading Section 1
      window.location.reload();
    } else if (phase === 'section1') {
      // Retry loading Section 2
      loadSection2();
    } else if (phase === 'section2' || phase === 'processing') {
      // Retry completing quiz
      completeQuiz();
    }
  };

  const handleComplete = () => {
    // Call parent completion handler
    onComplete();
  };

  // Show loading state
  if (loading && currentQuestions.length === 0) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center px-6">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-13 text-muted-foreground">
            {phase === 'processing' ? 'Generating your Taste DNA...' : 'Loading questions...'}
          </p>
        </div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center px-6">
        <div className="w-full max-w-md text-center">
          <div className="bg-surface/50 border border-red-500/20 rounded-lg p-8">
            <h2 className="text-20 font-medium text-foreground mb-3">Something went wrong</h2>
            <p className="text-13 text-muted-foreground mb-6">{error}</p>
            <button
              onClick={handleRetry}
              className="px-6 py-3 rounded-lg text-13 font-medium bg-white text-black hover:bg-white/90 transition-all duration-180"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Show Taste DNA card when complete
  if (phase === 'complete' && tasteDNA) {
    // Convert answers to format expected by TasteDNACard
    const answersForCard = {};
    [...section1Answers, ...section2Answers].forEach(answer => {
      const question = [...section1Questions, ...section2Questions].find(q => q.id === answer.questionId);
      if (question && question.category) {
        answersForCard[question.category] = answer.selectedOptions;
      }
    });
    
    return <TasteDNACard tasteDNA={tasteDNA} answers={answersForCard} onContinue={handleComplete} />;
  }

  // Show processing state
  if (phase === 'processing') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center px-6">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-13 text-muted-foreground">Generating your Taste DNA...</p>
        </div>
      </div>
    );
  }

  // Show question screen
  if (!currentQuestion) {
    return null;
  }

  const totalQuestions = section1Questions.length + section2Questions.length;
  const currentAbsoluteIndex = phase === 'section1' 
    ? currentQuestionIndex 
    : section1Questions.length + currentQuestionIndex;

  return (
    <QuestionScreen
      question={currentQuestion}
      currentIndex={currentAbsoluteIndex}
      totalQuestions={totalQuestions}
      selectedOptions={selectedOptions}
      onToggleOption={handleToggleOption}
      onNext={handleNext}
      loading={loading}
    />
  );
};

export default OnboardingPage;
