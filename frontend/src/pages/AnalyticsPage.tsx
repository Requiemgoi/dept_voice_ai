import React from 'react';
import { MainLayout } from '../components/layout/MainLayout';
import { useAnalytics } from '../hooks/useAnalytics';
import { Card } from '../components/ui/Card';
import {
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, Legend, AreaChart, Area
} from 'recharts';
import { Users, PhoneCall, CheckCircle, TrendingUp } from 'lucide-react';
import { CATEGORY_LABELS, CATEGORY_COLORS } from '../utils/constants';
import type { Category } from '../types/client';

const COLORS = ['#8b5cf6', '#22d3ee', '#10b981', '#f59e0b', '#ef4444', '#6366f1'];

export const AnalyticsPage: React.FC = () => {
    const { data: stats, isLoading } = useAnalytics();

    if (isLoading) {
        return (
            <MainLayout>
                <div className="p-8 flex items-center justify-center min-h-[400px]">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                </div>
            </MainLayout>
        );
    }

    const categoryData = stats ? Object.entries(stats.categories).map(([key, value]) => ({
        name: CATEGORY_LABELS[key as Category] || key,
        value: value,
        key: key as Category
    })) : [];

    return (
        <MainLayout>
            <div className="p-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Аналитика</h1>
                    <p className="text-gray-500 mt-1">Детальный обзор эффективности обзвонов</p>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-blue-100 rounded-lg">
                                <Users className="w-6 h-6 text-blue-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">База клиентов</p>
                                <p className="text-2xl font-bold">{stats?.summary.total_clients || 0}</p>
                            </div>
                        </div>
                    </Card>
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-purple-100 rounded-lg">
                                <PhoneCall className="w-6 h-6 text-purple-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Обработано</p>
                                <p className="text-2xl font-bold">{stats?.summary.completed || 0}</p>
                            </div>
                        </div>
                    </Card>
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-green-100 rounded-lg">
                                <CheckCircle className="w-6 h-6 text-green-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Конверсия</p>
                                <p className="text-2xl font-bold">{Math.round(stats?.summary.success_rate || 0)}%</p>
                            </div>
                        </div>
                    </Card>
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-orange-100 rounded-lg">
                                <TrendingUp className="w-6 h-6 text-orange-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">В процессе</p>
                                <p className="text-2xl font-bold">{stats?.summary.processing || 0}</p>
                            </div>
                        </div>
                    </Card>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Daily Activity Chart */}
                    <Card>
                        <h3 className="text-lg font-semibold mb-6">Активность за неделю</h3>
                        <div className="h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={stats?.daily_activity || []}>
                                    <defs>
                                        <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                                    <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 12 }} />
                                    <YAxis axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 12 }} />
                                    <Tooltip
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Area type="monotone" dataKey="count" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorCount)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </Card>

                    {/* Results Distribution */}
                    <Card>
                        <h3 className="text-lg font-semibold mb-6">Распределение ответов</h3>
                        <div className="h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={categoryData}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {categoryData.map((entry, index) => (
                                            <Cell
                                                key={`cell-${index}`}
                                                fill={CATEGORY_COLORS[entry.key] || COLORS[index % COLORS.length]}
                                            />
                                        ))}
                                    </Pie>
                                    <Tooltip
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Legend verticalAlign="bottom" height={36} />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </Card>
                </div>
            </div>
        </MainLayout>
    );
};
