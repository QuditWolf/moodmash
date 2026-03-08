export const onboardingQuestions = [
  {
    id: 'music',
    title: 'Pick music you vibe with',
    category: 'music',
    options: [
      'Indie Rock',
      'Hip Hop',
      'Bollywood',
      'Electronic',
      'Lo-fi',
      'Jazz',
      'Classical',
      'Alternative',
      'R&B',
      'Folk',
      'Metal',
      'Pop'
    ]
  },
  {
    id: 'movies',
    title: 'What films hit different?',
    category: 'movies',
    options: [
      'Psychological',
      'Sci-Fi',
      'Thriller',
      'Romance',
      'Documentary',
      'Anime',
      'Indie Cinema',
      'Art Films',
      'Horror',
      'Comedy',
      'Drama',
      'Action'
    ]
  },
  {
    id: 'books',
    title: 'Books that speak to you',
    category: 'books',
    options: [
      'Philosophy',
      'Sci-Fi',
      'Poetry',
      'Startups',
      'Psychology',
      'Fiction',
      'Biography',
      'Self-Help',
      'History',
      'Design',
      'Technology',
      'Fantasy'
    ]
  },
  {
    id: 'art',
    title: 'Art styles you appreciate',
    category: 'art',
    options: [
      'Abstract',
      'Minimalism',
      'Street Art',
      'Contemporary',
      'Digital Art',
      'Photography',
      'Illustration',
      'Sculpture',
      'Surrealism',
      'Pop Art',
      'Impressionism',
      'Conceptual'
    ]
  },
  {
    id: 'podcasts',
    title: 'Podcasts you listen to',
    category: 'podcasts',
    options: [
      'Tech Talks',
      'Design',
      'Startups',
      'Creative Process',
      'True Crime',
      'Comedy',
      'News',
      'Science',
      'Business',
      'Culture',
      'History',
      'Sports'
    ]
  },
  {
    id: 'articles',
    title: 'Topics you read about',
    category: 'articles',
    options: [
      'Product Strategy',
      'Design Systems',
      'Engineering',
      'Growth',
      'AI/ML',
      'Web3',
      'Leadership',
      'Marketing',
      'UX Research',
      'Data Science',
      'DevOps',
      'Productivity'
    ]
  },
  {
    id: 'creative',
    title: 'Creative interests',
    category: 'creative',
    options: [
      'Photography',
      'Writing',
      'Music Production',
      'Video Editing',
      'Graphic Design',
      'UI/UX Design',
      'Animation',
      '3D Modeling',
      'Illustration',
      'Game Dev',
      'Web Dev',
      'Architecture'
    ]
  },
  {
    id: 'mood',
    title: 'Content mood you prefer',
    category: 'mood',
    options: [
      'Inspiring',
      'Thought-provoking',
      'Relaxing',
      'Energetic',
      'Dark',
      'Uplifting',
      'Experimental',
      'Nostalgic',
      'Futuristic',
      'Raw',
      'Polished',
      'Authentic'
    ]
  },
  {
    id: 'format',
    title: 'How you consume content',
    category: 'format',
    options: [
      'Long reads',
      'Quick bites',
      'Visual first',
      'Audio',
      'Video',
      'Interactive',
      'Text heavy',
      'Image heavy',
      'Newsletters',
      'Threads',
      'Stories',
      'Deep dives'
    ]
  },
  {
    id: 'discovery',
    title: 'What drives your discovery',
    category: 'discovery',
    options: [
      'Trending',
      'Niche',
      'Curated',
      'Algorithmic',
      'Community picks',
      'Expert reviews',
      'Personal taste',
      'Serendipity',
      'Data-driven',
      'Recommendations',
      'Exploration',
      'Deep research'
    ]
  }
];

export const generateTasteDNA = (answers) => {
  // Simple archetype generation based on answers
  const totalSelections = Object.values(answers).flat().length;
  
  let archetype = 'The Explorer';
  if (totalSelections < 15) {
    archetype = 'The Minimalist';
  } else if (totalSelections > 30) {
    archetype = 'The Omnivore';
  } else if (answers.art?.length > 3 || answers.creative?.length > 3) {
    archetype = 'The Creative';
  } else if (answers.articles?.length > 3 || answers.books?.length > 3) {
    archetype = 'The Intellectual';
  }
  
  return {
    archetype,
    music: answers.music?.slice(0, 3).join(' / ') || 'Not specified',
    movies: answers.movies?.slice(0, 3).join(' / ') || 'Not specified',
    books: answers.books?.slice(0, 3).join(' / ') || 'Not specified',
    art: answers.art?.slice(0, 3).join(' / ') || 'Not specified',
    podcasts: answers.podcasts?.slice(0, 3).join(' / ') || 'Not specified',
  };
};
