import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import QuestionScreen from './QuestionScreen'
import { onboardingQuestions } from '../../data/onboardingQuestions'
import { api } from '../../services/api'
import { ArrowRight, Loader2 } from 'lucide-react'

const goalOptions = [
  'Build something that matters',
  'Get technically excellent',
  'Find what makes me happy',
  'Start something of my own',
  'Understand where I come from',
  'Just inspire me and see what emerges',
]

const OnboardingPage = () => {
  const navigate = useNavigate()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [phase, setPhase] = useState('questions') // 'questions' | 'goal' | 'submitting' | 'error'
  const [selectedGoal, setSelectedGoal] = useState(null)
  const [error, setError] = useState(null)

  const currentQuestion = onboardingQuestions[currentQuestionIndex]
  const selectedOptions = currentQuestion ? (answers[currentQuestion.id] || []) : []

  const handleToggleOption = (option) => {
    setAnswers((prev) => {
      const current = prev[currentQuestion.id] || []
      const isSelected = current.includes(option)
      return {
        ...prev,
        [currentQuestion.id]: isSelected
          ? current.filter((o) => o !== option)
          : [...current, option],
      }
    })
  }

  const handleNext = () => {
    if (currentQuestionIndex === onboardingQuestions.length - 1) {
      setPhase('goal')
    } else {
      setCurrentQuestionIndex((prev) => prev + 1)
    }
  }

  const handleSubmit = async () => {
    setPhase('submitting')
    setError(null)
    try {
      const result = await api.onboard(answers, selectedGoal)
      sessionStorage.setItem('session_id', result.session_id)
      navigate(`/dna/${result.session_id}`)
    } catch (err) {
      console.error('Onboarding error:', err)
      setError(err.message || 'Something went wrong. Please try again.')
      setPhase('error')
    }
  }

  // Loading / submitting state
  if (phase === 'submitting') {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <Loader2 className="w-6 h-6 text-muted-foreground animate-spin mb-4" />
        <p className="text-14 text-muted-foreground font-mono">
          Building your Taste DNA...
        </p>
      </div>
    )
  }

  // Error state
  if (phase === 'error') {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <p className="text-14 text-red-400 font-mono mb-6">{error}</p>
        <button
          onClick={() => setPhase('goal')}
          className="px-6 py-3 rounded-lg text-13 font-medium bg-white text-black hover:bg-white/90 transition-all duration-180 ease-out"
        >
          Try Again
        </button>
      </div>
    )
  }

  // Goal selection step
  if (phase === 'goal') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-4xl">
          <div className="mb-4">
            <span className="text-12 text-muted-foreground font-mono">
              Almost there
            </span>
          </div>

          <h1 className="text-28 font-medium tracking-tighter text-foreground mb-3">
            What's your north star right now?
          </h1>
          <p className="text-14 text-muted-foreground mb-10">
            This helps us tailor your growth path. Pick the one that resonates most.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-12">
            {goalOptions.map((goal) => (
              <button
                key={goal}
                onClick={() => setSelectedGoal(goal)}
                className={`
                  p-4 rounded-lg border text-left transition-all duration-180 ease-out text-13 font-mono
                  ${
                    selectedGoal === goal
                      ? 'bg-surface/80 border-white/20 text-foreground'
                      : 'bg-surface/50 border-white/10 text-muted-foreground hover:bg-surface/80 hover:border-white/20 hover:-translate-y-0.5'
                  }
                `}
              >
                {goal}
              </button>
            ))}
          </div>

          <div className="flex justify-between">
            <button
              onClick={() => {
                setPhase('questions')
              }}
              className="px-6 py-3 rounded-lg text-13 font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Back
            </button>
            <button
              onClick={handleSubmit}
              disabled={!selectedGoal}
              className={`
                flex items-center gap-2 px-6 py-3 rounded-lg text-13 font-medium transition-all duration-180 ease-out
                ${
                  selectedGoal
                    ? 'bg-white text-black hover:bg-white/90 hover:-translate-y-0.5'
                    : 'bg-surface/50 text-muted-foreground cursor-not-allowed'
                }
              `}
            >
              Build My Taste DNA
              <ArrowRight className="w-4 h-4" strokeWidth={2} />
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Questions phase
  return (
    <QuestionScreen
      question={currentQuestion}
      currentIndex={currentQuestionIndex}
      totalQuestions={onboardingQuestions.length}
      selectedOptions={selectedOptions}
      onToggleOption={handleToggleOption}
      onNext={handleNext}
    />
  )
}

export default OnboardingPage
