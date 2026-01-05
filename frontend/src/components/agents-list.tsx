"use client"

import { motion } from "framer-motion"
import { Phone, PhoneOff, Clock } from "lucide-react"

const agents = [
    {
        id: 1,
        name: "Agent Alpha",
        avatar: "AA",
        status: "active",
        calls: 142,
        successRate: 82,
    },
    {
        id: 2,
        name: "Agent Beta",
        avatar: "AB",
        status: "active",
        calls: 128,
        successRate: 78,
    },
    {
        id: 3,
        name: "Agent Gamma",
        avatar: "AG",
        status: "idle",
        calls: 95,
        successRate: 85,
    },
    {
        id: 4,
        name: "Agent Delta",
        avatar: "AD",
        status: "active",
        calls: 167,
        successRate: 76,
    },
    {
        id: 5,
        name: "Agent Epsilon",
        avatar: "AE",
        status: "offline",
        calls: 0,
        successRate: 0,
    },
]

const statusConfig = {
    active: {
        color: "bg-emerald-400",
        text: "text-emerald-400",
        icon: Phone,
        label: "On Call",
    },
    idle: {
        color: "bg-amber-400",
        text: "text-amber-400",
        icon: Clock,
        label: "Idle",
    },
    offline: {
        color: "bg-zinc-500",
        text: "text-zinc-500",
        icon: PhoneOff,
        label: "Offline",
    },
}

export function AgentsList() {
    return (
        <motion.div className="glass rounded-2xl p-6 border-purple-500/30" whileHover={{ scale: 1.005 }}>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="font-semibold text-lg text-white">AI Agents</h3>
                    <p className="text-sm text-muted-foreground">Real-time status</p>
                </div>
                <div className="flex items-center gap-2 text-xs">
                    <span className="flex items-center gap-1">
                        <div className="h-2 w-2 rounded-full bg-emerald-400" />
                        <span className="text-muted-foreground">Active</span>
                    </span>
                    <span className="flex items-center gap-1">
                        <div className="h-2 w-2 rounded-full bg-amber-400" />
                        <span className="text-muted-foreground">Idle</span>
                    </span>
                </div>
            </div>

            <div className="space-y-3">
                {agents.map((agent, index) => {
                    const status = statusConfig[agent.status as keyof typeof statusConfig]
                    const StatusIcon = status.icon

                    return (
                        <motion.div
                            key={agent.id}
                            className="glass rounded-xl p-4 flex items-center justify-between hover:border-purple-500/40 transition-colors cursor-pointer"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ x: 5 }}
                        >
                            <div className="flex items-center gap-3">
                                <div className="relative">
                                    <div className="h-10 w-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-sm font-bold text-white">
                                        {agent.avatar}
                                    </div>
                                    <div
                                        className={`absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full ${status.color} border-2 border-background`}
                                    />
                                </div>
                                <div>
                                    <h4 className="font-medium text-white text-sm">{agent.name}</h4>
                                    <div className="flex items-center gap-1">
                                        <StatusIcon className={`h-3 w-3 ${status.text}`} />
                                        <span className={`text-xs ${status.text}`}>{status.label}</span>
                                    </div>
                                </div>
                            </div>

                            <div className="text-right">
                                <p className="font-mono text-sm text-white">{agent.calls} calls</p>
                                <p className="text-xs text-muted-foreground">{agent.successRate}% success</p>
                            </div>
                        </motion.div>
                    )
                })}
            </div>
        </motion.div>
    )
}
