import React from 'react';
import { AnimatedBackground } from '../animated-background';
import { DashboardHeader } from '../dashboard-header';

interface MainLayoutProps {
    children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
    return (
        <div className="relative min-h-screen overflow-hidden bg-background text-foreground">
            <AnimatedBackground />

            <div className="relative z-10 flex flex-col min-h-screen">
                <DashboardHeader />

                <main className="flex-1 container mx-auto px-4 py-8">
                    {children}
                </main>
            </div>
        </div>
    );
};

