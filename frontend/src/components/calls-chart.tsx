"use client"

import { motion } from "framer-motion"
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

interface CallsChartProps {
    data?: Array<{ date: string; count: number }>;
}

export function CallsChart({ data }: CallsChartProps) {
    // Transform data for chart if needed
    const chartData = data?.map(d => ({
        time: d.date.split('-').slice(1).join('.'), // MM.DD
        calls: d.count,
        success: Math.round(d.count * 0.8) // Mock success for chart visual
    })) || [
            { time: "00:00", calls: 0, success: 0 },
        ];
    return (
        <motion.div className="glass rounded-2xl p-6 border-purple-500/30 h-full" whileHover={{ scale: 1.005 }}>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="font-semibold text-lg text-white">Call Activity</h3>
                    <p className="text-sm text-muted-foreground">Today&apos;s performance</p>
                </div>
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <div className="h-3 w-3 rounded-full bg-purple-500" />
                        <span className="text-xs text-muted-foreground">Total Calls</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="h-3 w-3 rounded-full bg-cyan-500" />
                        <span className="text-xs text-muted-foreground">Successful</span>
                    </div>
                </div>
            </div>

            <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <defs>
                            <linearGradient id="colorCalls" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorSuccess" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: "#71717a", fontSize: 12 }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717a", fontSize: 12 }} />
                        <Tooltip
                            content={({ active, payload, label }) => {
                                if (active && payload && payload.length) {
                                    return (
                                        <div className="glass-strong rounded-lg p-3 border border-purple-500/30">
                                            <p className="text-sm font-medium text-white mb-1">{label}</p>
                                            <p className="text-xs text-purple-400">Calls: {payload[0]?.value}</p>
                                            <p className="text-xs text-cyan-400">Success: {payload[1]?.value}</p>
                                        </div>
                                    )
                                }
                                return null
                            }}
                        />
                        <Area
                            type="monotone"
                            dataKey="calls"
                            stroke="#8b5cf6"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorCalls)"
                        />
                        <Area
                            type="monotone"
                            dataKey="success"
                            stroke="#22d3ee"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorSuccess)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </motion.div>
    )
}
