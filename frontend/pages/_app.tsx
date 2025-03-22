import type { AppProps } from 'next/app';
import { ClerkProvider } from '@clerk/nextjs';
import '../styles/globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider 
      afterSignInUrl="/dashboard"
      afterSignUpUrl="/dashboard"
    >
      <Component {...pageProps} />
    </ClerkProvider>
  );
}

export default MyApp; 