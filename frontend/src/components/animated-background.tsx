"use client"

import { useEffect, useRef } from "react"

export function AnimatedBackground() {
    const canvasRef = useRef<HTMLCanvasElement>(null)

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return

        const ctx = canvas.getContext("2d")
        if (!ctx) return

        let animationId: number
        const particles: Particle[] = []
        const particleCount = 80

        const resize = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
        }

        class Particle {
            x: number
            y: number
            size: number
            speedX: number
            speedY: number
            opacity: number
            color: string

            constructor() {
                this.x = Math.random() * canvas!.width
                this.y = Math.random() * canvas!.height
                this.size = Math.random() * 2 + 0.5
                this.speedX = (Math.random() - 0.5) * 0.5
                this.speedY = (Math.random() - 0.5) * 0.5
                this.opacity = Math.random() * 0.5 + 0.2
                const colors = ["139, 92, 246", "34, 211, 238", "236, 72, 153"]
                this.color = colors[Math.floor(Math.random() * colors.length)]
            }

            update() {
                this.x += this.speedX
                this.y += this.speedY

                if (this.x > canvas!.width) this.x = 0
                if (this.x < 0) this.x = canvas!.width
                if (this.y > canvas!.height) this.y = 0
                if (this.y < 0) this.y = canvas!.height
            }

            draw() {
                if (!ctx) return
                ctx.beginPath()
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
                ctx.fillStyle = `rgba(${this.color}, ${this.opacity})`
                ctx.fill()
            }
        }

        resize()
        window.addEventListener("resize", resize)

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle())
        }

        const animate = () => {
            ctx.fillStyle = "rgba(15, 10, 40, 0.05)"
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            particles.forEach((particle, i) => {
                particle.update()
                particle.draw()

                // Draw connections
                particles.slice(i + 1).forEach((otherParticle) => {
                    const dx = particle.x - otherParticle.x
                    const dy = particle.y - otherParticle.y
                    const distance = Math.sqrt(dx * dx + dy * dy)

                    if (distance < 150) {
                        ctx.beginPath()
                        ctx.strokeStyle = `rgba(139, 92, 246, ${0.1 * (1 - distance / 150)})`
                        ctx.lineWidth = 0.5
                        ctx.moveTo(particle.x, particle.y)
                        ctx.lineTo(otherParticle.x, otherParticle.y)
                        ctx.stroke()
                    }
                })
            })

            animationId = requestAnimationFrame(animate)
        }

        // Initial fill
        ctx.fillStyle = "#0f0a28"
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        animate()

        return () => {
            window.removeEventListener("resize", resize)
            cancelAnimationFrame(animationId)
        }
    }, [])

    return (
        <>
            <div className="fixed inset-0 animated-gradient" />
            <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none" style={{ mixBlendMode: "screen" }} />
            {/* Mesh gradient overlay */}
            <div
                className="fixed inset-0 opacity-30 pointer-events-none"
                style={{
                    background: `
            radial-gradient(ellipse at 20% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(34, 211, 238, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(236, 72, 153, 0.08) 0%, transparent 50%)
          `,
                }}
            />
        </>
    )
}
