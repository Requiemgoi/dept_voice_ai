"use client"

import { motion } from "framer-motion"
import { AnimatedBackground } from "@/components/animated-background"
import { DashboardHeader } from "@/components/dashboard-header"
import { StatsGrid } from "@/components/stats-grid"
import { LiveCallWidget } from "@/components/live-call-widget"
import { AIStatusCard } from "@/components/ai-status-card"
import { CallsChart } from "@/components/calls-chart"
import { AgentsList } from "@/components/agents-list"
import { RecentCalls } from "@/components/recent-calls"
import { useClients } from "@/hooks/useClients"
import { useAnalytics } from "@/hooks/useAnalytics"
import { useMemo } from "react"

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1,
            delayChildren: 0.2,
        },
    },
}

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
        opacity: 1,
        y: 0,
        transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
    },
}

export function Dashboard() {
    const { data: clientsData } = useClients({ limit: 10 });
    const { data: analyticsData } = useAnalytics();

    const stats = useMemo(() => {
        return {
            totalClients: analyticsData?.summary.total_clients || 0,
            activeCalls: analyticsData?.summary.processing || 0,
            successRate: Math.round(analyticsData?.summary.success_rate || 0),
            totalDebt: clientsData?.items.reduce((sum, c) => sum + (c.amount || 0), 0) || 0 // Approximation
        };
    }, [analyticsData, clientsData]);

    return (
        <div className="relative min-h-screen overflow-hidden bg-background text-foreground">
            <AnimatedBackground />

            <div className="relative z-10">
                <DashboardHeader />

                <motion.main
                    className="container mx-auto px-4 py-8 space-y-8"
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                >
                    {/* Stats Row */}
                    <motion.div variants={itemVariants}>
                        <StatsGrid stats={stats} />
                    </motion.div>

                    {/* Main Content Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Left Column - Live Call & AI Status */}
                        <motion.div variants={itemVariants} className="space-y-6">
                            <LiveCallWidget />
                            <AIStatusCard />
                        </motion.div>

                        {/* Center Column - Chart */}
                        <motion.div variants={itemVariants} className="lg:col-span-2">
                            <CallsChart data={analyticsData?.daily_activity} />
                        </motion.div>
                    </div>

                    {/* Bottom Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <motion.div variants={itemVariants}>
                            <AgentsList />
                        </motion.div>
                        <motion.div variants={itemVariants}>
                            <RecentCalls calls={clientsData?.items} />
                        </motion.div>
                    </div>
                </motion.main>
            </div>
        </div>
    )
}
