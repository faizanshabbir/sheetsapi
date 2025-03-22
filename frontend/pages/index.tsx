import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="container">
        <h1>Welcome to Sheets API Generator</h1>
        <p>Create APIs from your Google Sheets with just a few clicks.</p>
        
        <div className="actions">
          <a href="/dashboard" className="button">
            Go to Dashboard
          </a>
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
            border-radius: 5px;
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