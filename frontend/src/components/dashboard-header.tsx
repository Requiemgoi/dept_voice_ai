"use client"

import { motion } from "framer-motion"
import { Bell, Settings, Search, Zap, Users, Phone, FileText, TrendingUp, BarChart3 } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/input"
import { Link, useLocation } from "react-router-dom"
import { cn } from "@/utils/cn"

export function DashboardHeader() {
    const location = useLocation();

    const menuItems = [
        { icon: BarChart3, label: 'Дашборд', path: '/' },
        { icon: Users, label: 'Клиенты', path: '/clients' },
        { icon: Phone, label: 'История', path: '/history' },
        { icon: FileText, label: 'Отчеты', path: '/reports' },
        { icon: TrendingUp, label: 'Аналитика', path: '/analytics' },
    ];

    return (
        <motion.header
            className="glass-strong sticky top-0 z-50 border-b border-purple-500/20"
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-8">
                        {/* Logo */}
                        <div className="flex items-center gap-3">
                            <motion.div
                                className="relative h-10 w-10 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 p-0.5"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <div className="flex h-full w-full items-center justify-center rounded-xl bg-background/80">
                                    <Zap className="h-5 w-5 text-purple-400" />
                                </div>
                            </motion.div>
                            <div>
                                <h1 className="font-[family-name:var(--font-space)] text-xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                                    MNB Collection
                                </h1>
                                <p className="text-[10px] uppercase tracking-widest text-muted-foreground">AI Calling System</p>
                            </div>
                        </div>

                        {/* Navigation */}
                        <nav className="hidden lg:flex items-center gap-1">
                            {menuItems.map((item) => (
                                <Link key={item.path} to={item.path}>
                                    <Button
                                        variant="ghost"
                                        className={cn(
                                            "gap-2 text-muted-foreground hover:text-white hover:bg-white/5",
                                            location.pathname === item.path && "text-white bg-white/10"
                                        )}
                                    >
                                        <item.icon className="h-4 w-4" />
                                        {item.label}
                                    </Button>
                                </Link>
                            ))}
                        </nav>
                    </div>

                    {/* Search */}
                    <div className="hidden md:flex flex-1 max-w-sm mx-4">
                        <div className="relative w-full">
                            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                            <Input
                                placeholder="Поиск клиентов..."
                                className="pl-10 glass border-purple-500/20 focus:border-purple-500/50 focus:ring-purple-500/20"
                            />
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-2">
                        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                            <Button variant="ghost" size="icon" className="relative hover:bg-purple-500/10">
                                <Bell className="h-5 w-5 text-muted-foreground" />
                                <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
                            </Button>
                        </motion.div>

                        <Link to="/settings">
                            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                                <Button variant="ghost" size="icon" className="hover:bg-purple-500/10">
                                    <Settings className="h-5 w-5 text-muted-foreground" />
                                </Button>
                            </motion.div>
                        </Link>

                        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                            <Button className="ml-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white border-0 neon-glow">
                                <Zap className="h-4 w-4 mr-2" />
                                Новый обзвон
                            </Button>
                        </motion.div>
                    </div>
                </div>
            </div>
        </motion.header>
    )
}
