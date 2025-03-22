import Layout from '../components/Layout';
import { useRouter } from 'next/router';
import { useAuth } from '@clerk/nextjs';

export default function Dashboard() {
  const { isLoaded, isSignedIn } = useAuth();
  const router = useRouter();

  // Redirect to home if not signed in
  if (isLoaded && !isSignedIn) {
    router.push('/');
    return null;
  }

  return (
    <Layout>
      <div className="container">
        <h1>Dashboard</h1>
        <div className="card">
          <h2>Your APIs</h2>
          <p>No APIs created yet.</p>
          <button className="button">Create New API</button>
        </div>

        <style jsx>{`
          .container {
            padding: 2rem;
          }
          .card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 2rem;
          }
          .button {
            margin-top: 1rem;
            padding: 0.8rem 1.5rem;
            background: #0070f3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.2s;
          }
          .button:hover {
            background: #0051b3;
          }
        `}</style>
      </div>
    </Layout>
  );
} 