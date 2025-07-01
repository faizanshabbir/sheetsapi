import { useEffect, useState } from 'react';
import { useUser, useAuth } from '@clerk/nextjs';
import Layout from '../components/Layout';

interface Sheet {
  id: string;
  name: string;
  endpoint_path: string;
  created_at: string;
}

export default function Dashboard() {
  const { user, isLoaded } = useUser();
  const { getToken } = useAuth();
  const [sheets, setSheets] = useState<Sheet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (isLoaded && user) {
      fetchSheets();
    }
  }, [isLoaded, user]);

  const fetchSheets = async () => {
    try {
      setLoading(true);
      const token = await getToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/sheets`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch sheets');
      }

      const data = await response.json();
      
      // Ensure data is an array
      if (Array.isArray(data)) {
        setSheets(data);
      } else {
        console.error('Unexpected data format:', data);
        setSheets([]);
        setError('Received invalid data format from server');
      }
    } catch (error) {
      console.error('Error fetching sheets:', error);
      setError(error instanceof Error ? error.message : 'An error occurred');
      setSheets([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="dashboard">
        <h1>Your API Endpoints</h1>
        <button
          onClick={() => window.location.href = '/sheets/new'}
          className="create-btn"
        >
          Create New API
        </button>

        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : sheets.length === 0 ? (
          <p>No APIs created yet. Create your first one!</p>
        ) : (
          <div className="sheets-grid">
            {sheets.map((sheet) => (
              <div key={sheet.id} className="sheet-card">
                <h3>{sheet.name}</h3>
                <p>Endpoint: {sheet.endpoint_path}</p>
                <p>Created: {new Date(sheet.created_at).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        )}

        <style jsx>{`
          .dashboard {
            padding: 2rem 0;
          }
          .create-btn {
            background: #0070f3;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 2rem;
          }
          .sheets-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
          }
          .sheet-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #eaeaea;
          }
          .error {
            color: red;
            margin: 1rem 0;
          }
        `}</style>
      </div>
    </Layout>
  );
} 