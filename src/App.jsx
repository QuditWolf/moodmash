import Sidebar from './components/Sidebar';
import FeedPage from './components/FeedPage';

function App() {
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
