"use client"

import { motion } from "framer-motion"

interface VoiceWaveformProps {
    isActive: boolean
}

export function VoiceWaveform({ isActive }: VoiceWaveformProps) {
    const bars = 40

    return (
        <div className="flex items-center justify-center gap-[2px] h-full">
            {Array.from({ length: bars }).map((_, i) => {
                const delay = i * 0.05
                const baseHeight = Math.sin(i * 0.3) * 0.3 + 0.4

                return (
                    <motion.div
                        key={i}
                        className="w-1 rounded-full bg-gradient-to-t from-purple-500 via-pink-500 to-cyan-400"
                        initial={{ height: "20%" }}
                        animate={
                            isActive
                                ? {
                                    height: [
                                        `${baseHeight * 30}%`,
                                        `${baseHeight * 100}%`,
                                        `${baseHeight * 50}%`,
                                        `${baseHeight * 80}%`,
                                        `${baseHeight * 30}%`,
                                    ],
                                }
                                : { height: "10%" }
                        }
                        transition={
                            isActive
                                ? {
                                    duration: 0.8 + Math.random() * 0.4,
                                    repeat: Number.POSITIVE_INFINITY,
                                    repeatType: "reverse",
                                    delay: delay,
                                    ease: "easeInOut",
                                }
                                : { duration: 0.3 }
                        }
                        style={{
                            boxShadow: isActive ? "0 0 10px rgba(139, 92, 246, 0.5)" : "none",
                        }}
                    />
                )
            })}
        </div>
    )
}
