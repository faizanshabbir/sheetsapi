import { useState } from 'react';
import { useUser, useAuth } from '@clerk/nextjs';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';

export default function NewSheet() {
  const { user } = useUser();
  const { getToken } = useAuth();
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    sheet_url: '',
    sheet_range: 'A1:Z1000',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const token = await getToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/sheets`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create API');
      }

      router.push('/dashboard');
    } catch (error: any) {
      setError(error?.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="new-sheet">
        <h1>Create New API</h1>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">API Name</label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="sheet_url">Google Sheet URL</label>
            <input
              type="text"
              id="sheet_url"
              value={formData.sheet_url}
              onChange={(e) => setFormData({ ...formData, sheet_url: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="sheet_range">Sheet Range (optional)</label>
            <input
              type="text"
              id="sheet_range"
              value={formData.sheet_range}
              onChange={(e) => setFormData({ ...formData, sheet_range: e.target.value })}
            />
          </div>

          {error && <div className="error">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create API'}
          </button>
        </form>

        <style jsx>{`
          .new-sheet {
            max-width: 600px;
            margin: 0 auto;
            padding: 2rem 0;
          }
          .form-group {
            margin-bottom: 1rem;
          }
          label {
            display: block;
            margin-bottom: 0.5rem;
          }
          input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
          }
          button {
            background: #0070f3;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
          }
          button:disabled {
            opacity: 0.5;
          }
          .error {
            color: red;
            margin-top: 1rem;
          }
        `}</style>
      </div>
    </Layout>
  );
} 