"use client"

import { motion } from "framer-motion"
import { Phone, DollarSign, TrendingUp, Users } from "lucide-react"
import { AnimatedCounter } from "@/components/animated-counter"

interface DashboardStats {
    totalClients: number;
    activeCalls: number;
    successRate: number;
    totalDebt: number;
}

interface StatsGridProps {
    stats?: DashboardStats;
}

const colorMap = {
    purple: {
        bg: "from-purple-500/20 to-purple-600/10",
        border: "border-purple-500/30",
        icon: "text-purple-400",
        glow: "neon-glow",
    },
    cyan: {
        bg: "from-cyan-500/20 to-cyan-600/10",
        border: "border-cyan-500/30",
        icon: "text-cyan-400",
        glow: "neon-glow-cyan",
    },
    pink: {
        bg: "from-pink-500/20 to-pink-600/10",
        border: "border-pink-500/30",
        icon: "text-pink-400",
        glow: "neon-glow-pink",
    },
    emerald: {
        bg: "from-emerald-500/20 to-emerald-600/10",
        border: "border-emerald-500/30",
        icon: "text-emerald-400",
        glow: "neon-glow", // Reuse glow or define new one
    }
}

export function StatsGrid({ stats }: StatsGridProps) {
    const data = [
        {
            label: "Всего клиентов",
            value: stats?.totalClients || 0,
            change: "База данных",
            positive: true,
            icon: Users,
            color: "purple",
        },
        {
            label: "Общая сумма долга",
            value: stats?.totalDebt || 0,
            prefix: "₸",
            change: "В обработке",
            positive: true,
            icon: DollarSign,
            color: "cyan",
        },
        {
            label: "Успешность (AI)",
            value: stats?.successRate || 0,
            suffix: "%",
            change: "Точность модели",
            positive: true,
            icon: TrendingUp,
            color: "pink",
        },
        {
            label: "Активные звонки",
            value: stats?.activeCalls || 0,
            change: "В реальном времени",
            positive: true,
            icon: Phone,
            color: "emerald",
        },
    ]

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {data.map((stat, index) => {
                const colors = colorMap[stat.color as keyof typeof colorMap] || colorMap.purple
                return (
                    <motion.div
                        key={stat.label}
                        className={`glass rounded-2xl p-6 ${colors.border} hover:${colors.glow} transition-shadow duration-500`}
                        whileHover={{ y: -5, scale: 1.02 }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                    >
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">{stat.label}</p>
                                <div className="flex items-baseline gap-1">
                                    {stat.prefix && <span className="text-2xl font-bold text-muted-foreground">{stat.prefix}</span>}
                                    <span className="font-[family-name:var(--font-space)] text-4xl font-bold bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">
                                        <AnimatedCounter value={stat.value} />
                                    </span>
                                    {stat.suffix && <span className="text-2xl font-bold text-muted-foreground">{stat.suffix}</span>}
                                </div>
                                <div className={`mt-2 text-xs ${stat.positive ? "text-emerald-400" : "text-muted-foreground"}`}>
                                    {stat.change}
                                </div>
                            </div>
                            <div className={`p-3 rounded-xl bg-gradient-to-br ${colors.bg}`}>
                                <stat.icon className={`h-6 w-6 ${colors.icon}`} />
                            </div>
                        </div>
                    </motion.div>
                )
            })}
        </div>
    )
}
