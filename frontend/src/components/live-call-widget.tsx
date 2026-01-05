"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Phone, Mic, Volume2 } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { VoiceWaveform } from "@/components/voice-waveform"

export function LiveCallWidget() {
    const [isLive, setIsLive] = useState(true)
    const [duration, setDuration] = useState(127)

    useEffect(() => {
        if (isLive) {
            const interval = setInterval(() => {
                setDuration((d) => d + 1)
            }, 1000)
            return () => clearInterval(interval)
        }
    }, [isLive])

    const formatDuration = (seconds: number) => {
        const mins = Math.floor(seconds / 60)
        const secs = seconds % 60
        return `${mins}:${secs.toString().padStart(2, "0")}`
    }

    return (
        <motion.div
            className="glass rounded-2xl p-6 border-purple-500/30 overflow-hidden relative"
            whileHover={{ scale: 1.01 }}
        >
            {/* Animated border glow */}
            <div className="absolute inset-0 rounded-2xl opacity-50">
                <div className="absolute inset-0 rounded-2xl animate-pulse bg-gradient-to-r from-purple-500/20 via-pink-500/20 to-cyan-500/20" />
            </div>

            <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <div className="relative">
                            <div className="h-3 w-3 rounded-full bg-emerald-400 animate-pulse" />
                            <div className="absolute inset-0 h-3 w-3 rounded-full bg-emerald-400 animate-ping" />
                        </div>
                        <span className="text-sm font-medium text-emerald-400">LIVE CALL</span>
                    </div>
                    <span className="font-mono text-lg text-purple-400">{formatDuration(duration)}</span>
                </div>

                {/* Client Info */}
                <div className="flex items-center gap-4 mb-6">
                    <div className="h-14 w-14 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xl font-bold text-white">
                        JD
                    </div>
                    <div>
                        <h3 className="font-semibold text-lg text-white">John Doe</h3>
                        <p className="text-sm text-muted-foreground">Account #4892-7231</p>
                        <p className="text-xs text-pink-400">Outstanding: $2,450.00</p>
                    </div>
                </div>

                {/* Voice Waveform */}
                <div className="h-20 mb-6">
                    <VoiceWaveform isActive={isLive} />
                </div>

                {/* Controls */}
                <div className="flex items-center justify-center gap-4">
                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-12 w-12 rounded-full border-purple-500/30 hover:bg-purple-500/20 bg-transparent"
                        >
                            <Mic className="h-5 w-5 text-purple-400" />
                        </Button>
                    </motion.div>
                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                        <Button
                            size="icon"
                            className="h-14 w-14 rounded-full bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-400 hover:to-pink-400 neon-glow-pink"
                            onClick={() => setIsLive(!isLive)}
                        >
                            <Phone className="h-6 w-6 text-white" />
                        </Button>
                    </motion.div>
                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-12 w-12 rounded-full border-purple-500/30 hover:bg-purple-500/20 bg-transparent"
                        >
                            <Volume2 className="h-5 w-5 text-purple-400" />
                        </Button>
                    </motion.div>
                </div>
            </div>
        </motion.div>
    )
}
