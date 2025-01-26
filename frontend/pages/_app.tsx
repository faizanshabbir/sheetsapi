import { ClerkProvider } from '@clerk/nextjs';
import type { AppProps } from 'next/app';
import Layout from '../components/Layout';
import '../styles/globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </ClerkProvider>
  );
}

export default MyApp; 