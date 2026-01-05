"use client"

import { motion } from "framer-motion"
import { Phone, Clock, ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Link } from "react-router-dom"
import type { Client } from "@/types/client"
import { formatDistanceToNow } from "date-fns"
import { ru } from "date-fns/locale"

interface RecentCallsProps {
    calls?: Client[];
}

export function RecentCalls({ calls = [] }: RecentCallsProps) {
    // Use first 5 calls
    const recentCalls = calls.slice(0, 5);

    return (
        <div className="glass rounded-2xl p-6 border-purple-500/20 h-full">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="font-[family-name:var(--font-space)] text-lg font-bold">Последние звонки</h3>
                    <p className="text-sm text-muted-foreground">История активности AI</p>
                </div>
                <Link to="/history">
                    <Button variant="ghost" size="sm" className="bg-white/5 hover:bg-white/10">
                        Все звонки <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </Link>
            </div>

            <div className="space-y-4">
                {recentCalls.length === 0 ? (
                    <div className="text-center text-muted-foreground py-8">
                        Нет последних звонков
                    </div>
                ) : (
                    recentCalls.map((call, index) => (
                        <motion.div
                            key={call.id}
                            className="group flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors border border-transparent hover:border-purple-500/20"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <div className="flex items-center gap-4">
                                <div
                                    className={`p-2 rounded-lg ${call.status === "completed"
                                            ? "bg-emerald-500/10 text-emerald-400"
                                            : call.status === "failed"
                                                ? "bg-red-500/10 text-red-400"
                                                : "bg-blue-500/10 text-blue-400"
                                        }`}
                                >
                                    <Phone className="h-4 w-4" />
                                </div>
                                <div>
                                    <h4 className="font-medium text-sm text-white">{call.fio}</h4>
                                    <p className="text-xs text-muted-foreground">{call.phone}</p>
                                </div>
                            </div>

                            <div className="flex items-center gap-6">
                                <div className="hidden sm:flex items-center gap-2 text-xs text-muted-foreground">
                                    <Clock className="h-3 w-3" />
                                    {call.processed_at ? formatDistanceToNow(new Date(call.processed_at), { addSuffix: true, locale: ru }) : "Не обработан"}
                                </div>
                                <div
                                    className={`px-3 py-1 rounded-full text-xs font-medium border ${call.status === "completed"
                                            ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
                                            : call.status === "failed"
                                                ? "bg-red-500/10 border-red-500/20 text-red-400"
                                                : "bg-blue-500/10 border-blue-500/20 text-blue-400"
                                        }`}
                                >
                                    {call.status === "completed" && "Успешно"}
                                    {call.status === "failed" && "Неудачно"}
                                    {call.status === "pending" && "Ожидание"}
                                    {call.status === "processing" && "Звонок..."}
                                </div>
                            </div>
                        </motion.div>
                    ))
                )}
            </div>
        </div>
    )
}
