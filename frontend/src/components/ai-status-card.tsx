"use client"

import { motion } from "framer-motion"
import { Brain, Cpu, Activity } from "lucide-react"
import { NeonProgressBar } from "@/components/neon-progress-bar"

export function AIStatusCard() {
    return (
        <motion.div className="glass rounded-2xl p-6 border-cyan-500/30" whileHover={{ scale: 1.01 }}>
            <div className="flex items-center gap-3 mb-6">
                <div className="relative">
                    <div className="p-3 rounded-xl bg-gradient-to-br from-cyan-500/20 to-cyan-600/10">
                        <Brain className="h-6 w-6 text-cyan-400" />
                    </div>
                    {/* Animated pulse ring */}
                    <motion.div
                        className="absolute inset-0 rounded-xl border-2 border-cyan-400"
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.5, 0, 0.5],
                        }}
                        transition={{
                            duration: 2,
                            repeat: Number.POSITIVE_INFINITY,
                            ease: "easeInOut",
                        }}
                    />
                </div>
                <div>
                    <h3 className="font-semibold text-white">AI Engine Status</h3>
                    <p className="text-xs text-emerald-400">All Systems Operational</p>
                </div>
            </div>

            <div className="space-y-4">
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                            <Cpu className="h-4 w-4 text-purple-400" />
                            <span className="text-sm text-muted-foreground">Processing Power</span>
                        </div>
                        <span className="text-sm font-mono text-purple-400">87%</span>
                    </div>
                    <NeonProgressBar value={87} color="purple" />
                </div>

                <div>
                    <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                            <Activity className="h-4 w-4 text-cyan-400" />
                            <span className="text-sm text-muted-foreground">Model Confidence</span>
                        </div>
                        <span className="text-sm font-mono text-cyan-400">94%</span>
                    </div>
                    <NeonProgressBar value={94} color="cyan" />
                </div>

                <div>
                    <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                            <Brain className="h-4 w-4 text-pink-400" />
                            <span className="text-sm text-muted-foreground">Learning Rate</span>
                        </div>
                        <span className="text-sm font-mono text-pink-400">72%</span>
                    </div>
                    <NeonProgressBar value={72} color="pink" />
                </div>
            </div>

            {/* Status indicators */}
            <div className="mt-6 pt-4 border-t border-purple-500/20">
                <div className="grid grid-cols-3 gap-2 text-center">
                    {[
                        { label: "NLP", status: "Active" },
                        { label: "Voice", status: "Active" },
                        { label: "Sentiment", status: "Active" },
                    ].map((item) => (
                        <div key={item.label} className="glass rounded-lg p-2">
                            <p className="text-[10px] text-muted-foreground uppercase tracking-wider">{item.label}</p>
                            <p className="text-xs text-emerald-400 font-medium">{item.status}</p>
                        </div>
                    ))}
                </div>
            </div>
        </motion.div>
    )
}
