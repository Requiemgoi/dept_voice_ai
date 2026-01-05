"use client"

import { motion } from "framer-motion"

interface NeonProgressBarProps {
    value: number
    color: "purple" | "cyan" | "pink"
}

const colorMap = {
    purple: {
        bg: "bg-purple-500/20",
        fill: "bg-gradient-to-r from-purple-600 to-purple-400",
        glow: "shadow-[0_0_10px_rgba(139,92,246,0.5),0_0_20px_rgba(139,92,246,0.3)]",
    },
    cyan: {
        bg: "bg-cyan-500/20",
        fill: "bg-gradient-to-r from-cyan-600 to-cyan-400",
        glow: "shadow-[0_0_10px_rgba(34,211,238,0.5),0_0_20px_rgba(34,211,238,0.3)]",
    },
    pink: {
        bg: "bg-pink-500/20",
        fill: "bg-gradient-to-r from-pink-600 to-pink-400",
        glow: "shadow-[0_0_10px_rgba(236,72,153,0.5),0_0_20px_rgba(236,72,153,0.3)]",
    },
}

export function NeonProgressBar({ value, color }: NeonProgressBarProps) {
    const colors = colorMap[color]

    return (
        <div className={`h-2 rounded-full ${colors.bg} overflow-hidden`}>
            <motion.div
                className={`h-full rounded-full ${colors.fill} ${colors.glow}`}
                initial={{ width: 0 }}
                animate={{ width: `${value}%` }}
                transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
            />
        </div>
    )
}
