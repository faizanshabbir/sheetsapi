import Layout from '../components/Layout';
import { SignInButton, useAuth } from '@clerk/nextjs';
import { useRouter } from 'next/router';

export default function Home() {
  const { isSignedIn } = useAuth();
  const router = useRouter();

  return (
    <Layout>
      <div className="container">
        <h1>Welcome to Sheets API Generator</h1>
        <p>Create APIs from your Google Sheets with just a few clicks.</p>
        
        <div className="actions">
          {isSignedIn ? (
            <button 
              className="button"
              onClick={() => router.push('/dashboard')}
            >
              Go to Dashboard
            </button>
          ) : (
            <SignInButton mode="modal">
              <button className="button">
                Sign In to Get Started
              </button>
            </SignInButton>
          )}
        </div>

        <style jsx>{`
          .container {
            padding: 2rem;
            text-align: center;
          }
          .actions {
            margin-top: 2rem;
          }
          .button {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: #0070f3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.2s;
            font-size: 1rem;
          }
          .button:hover {
            background: #0051b3;
          }
        `}</style>
      </div>
    </Layout>
  );
} 