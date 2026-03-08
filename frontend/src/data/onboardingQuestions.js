export const onboardingQuestions = [
  // Music (2 questions)
  {
    id: 'music_vibe',
    domain: 'music',
    title: 'Pick songs that match your vibe',
    options: [
      'Prateek Kuhad - cold/mess',
      'AR Rahman - Kun Faya Kun',
      'Nucleya - Bass Rani',
      'Anuv Jain - BAARISHEIN',
      'King - Maan Meri Jaan',
      'Indian Ocean - Kandisa',
      'Ritviz - Udd Gaye',
      'Cigarettes After Sex',
    ],
  },
  {
    id: 'music_mood',
    domain: 'music',
    title: 'Your go-to music mood',
    options: [
      'Introspective indie',
      'High-energy electronic',
      'Soulful classics',
      'Regional roots',
      'Chill lo-fi beats',
      'Live acoustic sessions',
    ],
  },

  // Films (2 questions)
  {
    id: 'film_picks',
    domain: 'films',
    title: 'Films that hit different',
    options: [
      'Masaan',
      'Dil Chahta Hai',
      'Gangs of Wasseypur',
      'Tumbbad',
      'The Lunchbox',
      'Ship of Theseus',
      'Udaan',
      'Pather Panchali',
    ],
  },
  {
    id: 'story_theme',
    domain: 'films',
    title: 'Stories you connect with',
    options: [
      'Identity and belonging',
      'Love and relationships',
      'Ambition and hustle',
      'Mystery and thriller',
      'Cultural roots',
      'Everyday magic',
    ],
  },

  // Visual & Creative (2 questions)
  {
    id: 'visual_style',
    domain: 'visual',
    title: 'Your aesthetic vibe',
    options: [
      'Minimalist and clean',
      'Maximalist Indian textiles',
      'Vintage and retro',
      'Modern brutalist',
      'Nature and organic',
      'Pop art and bold colors',
    ],
  },
  {
    id: 'creative_time',
    domain: 'creative',
    title: 'In your free time, you...',
    options: [
      'Create something new',
      'Deep dive into content',
      'Learn new skills',
      'Connect with people',
      'Think and reflect',
      'Explore and discover',
    ],
  },

  // Books & Goals (2 questions)
  {
    id: 'books_interest',
    domain: 'creative',
    title: 'Books that interest you',
    options: [
      'Fiction and novels',
      'Philosophy and essays',
      'Self-help and growth',
      'Biographies',
      'Poetry',
      'Business and startups',
    ],
  },
  {
    id: 'content_changed',
    domain: 'consumption',
    title: 'Content that changed you',
    options: [
      'A powerful film scene',
      'An eye-opening essay',
      'A life-defining album',
      'A creator\'s entire work',
      'A meaningful conversation',
      'A skill that unlocked others',
    ],
  },
]

export const goalOptions = [
  'Build something that matters',
  'Get technically excellent',
  'Find what makes me happy',
  'Start something of my own',
  'Understand where I come from',
  'Just inspire me and see what emerges',
]

export const generateTasteDNA = (answers) => {
  // Simple archetype generation for backward compatibility
  const allAnswers = Object.values(answers).flat()
  const totalSelections = allAnswers.length

  // Domain counts
  const domainCounts = {}
  onboardingQuestions.forEach((q) => {
    const a = answers[q.id] || []
    domainCounts[q.domain] = (domainCounts[q.domain] || 0) + a.length
  })

  const topDomain = Object.entries(domainCounts).sort((a, b) => b[1] - a[1])[0]?.[0]

  let archetype = 'The Explorer'
  if (totalSelections < 10) {
    archetype = 'The Minimalist'
  } else if (totalSelections > 25) {
    archetype = 'The Omnivore'
  } else if (topDomain === 'visual' || topDomain === 'creative') {
    archetype = 'The Creative'
  } else if (topDomain === 'films' || topDomain === 'consumption') {
    archetype = 'The Intellectual'
  }

  return {
    archetype,
    domains: domainCounts,
    topSelections: allAnswers.slice(0, 5),
  }
}
