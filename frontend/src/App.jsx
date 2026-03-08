import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import FeedPage from './components/FeedPage';
import OnboardingPage from './components/onboarding/OnboardingPage';

function App() {
  const [showOnboarding, setShowOnboarding] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user has completed onboarding
    const tasteProfile = localStorage.getItem('taste_profile');
    if (tasteProfile) {
      setShowOnboarding(false);
    }
    setIsLoading(false);
  }, []);

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-13 text-muted-foreground font-mono">Loading...</div>
      </div>
    );
  }

  if (showOnboarding) {
    return <OnboardingPage onComplete={handleOnboardingComplete} />;
  }

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <main className="flex-1 ml-64">
        <FeedPage />
      </main>
    </div>
  );
}

export default App;
