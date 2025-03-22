import React from 'react';
import { UserButton } from "@clerk/nextjs";
import { useRouter } from "next/router";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();

  return (
    <div className="layout">
      <header>
        <nav>
          <div className="logo" onClick={() => router.push('/')}>
            Sheets API Generator
          </div>
          <div className="nav-right">
            <UserButton afterSignOutUrl="/"/>
          </div>
        </nav>
      </header>

      <main>
        {children}
      </main>

      <style jsx>{`
        .layout {
          min-height: 100vh;
        }
        header {
          background: white;
          border-bottom: 1px solid #eaeaea;
          margin-bottom: 2rem;
        }
        nav {
          max-width: 1200px;
          margin: 0 auto;
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .logo {
          font-size: 1.5rem;
          font-weight: bold;
          cursor: pointer;
        }
        main {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 2rem;
        }
      `}</style>
    </div>
  );
} 