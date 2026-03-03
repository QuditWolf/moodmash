import { useState } from 'react';
import QuestionScreen from './QuestionScreen';
import TasteDNACard from './TasteDNACard';
import { onboardingQuestions, generateTasteDNA } from '../../data/onboardingQuestions';

const OnboardingPage = ({ onComplete }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showTasteDNA, setShowTasteDNA] = useState(false);
  const [tasteDNA, setTasteDNA] = useState(null);

  const currentQuestion = onboardingQuestions[currentQuestionIndex];
  const selectedOptions = answers[currentQuestion.id] || [];

  const handleToggleOption = (option) => {
    setAnswers(prev => {
      const currentSelections = prev[currentQuestion.id] || [];
      const isSelected = currentSelections.includes(option);

      return {
        ...prev,
        [currentQuestion.id]: isSelected
          ? currentSelections.filter(o => o !== option)
          : [...currentSelections, option]
      };
    });
  };

  const handleNext = () => {
    if (currentQuestionIndex === onboardingQuestions.length - 1) {
      // Last question - generate Taste DNA
      const dna = generateTasteDNA(answers);
      setTasteDNA(dna);
      setShowTasteDNA(true);
    } else {
      // Move to next question
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handleComplete = () => {
    // Store in localStorage
    localStorage.setItem('taste_profile', JSON.stringify({
      answers,
      tasteDNA,
      completedAt: new Date().toISOString()
    }));

    // Call parent completion handler
    onComplete();
  };

  if (showTasteDNA && tasteDNA) {
    return <TasteDNACard tasteDNA={tasteDNA} answers={answers} onContinue={handleComplete} />;
  }

  return (
    <QuestionScreen
      question={currentQuestion}
      currentIndex={currentQuestionIndex}
      totalQuestions={onboardingQuestions.length}
      selectedOptions={selectedOptions}
      onToggleOption={handleToggleOption}
      onNext={handleNext}
    />
  );
};

export default OnboardingPage;
