import { Link } from 'react-router-dom'

const NotFound = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6 font-mono">
      <h1 className="text-6xl font-medium tracking-tighter text-foreground">
        404
      </h1>
      <p className="text-sm text-muted-foreground mt-2 mb-8">
        Page not found.
      </p>
      <Link
        to="/"
        className="px-6 py-3 rounded-lg text-sm font-medium bg-white text-black hover:bg-white/90 hover:-translate-y-0.5 transition-all duration-180 ease-out"
      >
        Back to Home
      </Link>
    </div>
  )
}

export default NotFound
