import React from 'react';
import { NavLink } from 'react-router-dom';
import {
    Phone,
    FileText,
    Users,
    TrendingUp,
    BarChart3,
    Settings,
} from 'lucide-react';
import clsx from 'clsx';

interface SidebarProps {
    className?: string;
    onSettingsClick?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ className }) => {
    const menuItems = [
        { icon: BarChart3, label: 'Дашборд', path: '/' },
        { icon: Users, label: 'Клиенты', path: '/clients' },
        { icon: Phone, label: 'История звонков', path: '/history' },
        { icon: FileText, label: 'Отчеты', path: '/reports' },
        { icon: TrendingUp, label: 'Аналитика', path: '/analytics' },
        { icon: Settings, label: 'Настройки', path: '/settings' },
    ];

    return (
        <aside className={clsx('w-64 bg-primary-900 text-white flex flex-col', className)}>
            {/* Logo */}
            <div className="p-6 border-b border-primary-800">
                <h1 className="text-2xl font-bold">MNB Collection</h1>
                <p className="text-sm text-primary-300 mt-1">AI Calling System</p>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4">
                <ul className="space-y-2">
                    {menuItems.map((item, index) => (
                        <li key={index}>
                            <NavLink
                                to={item.path}
                                className={({ isActive }) =>
                                    clsx(
                                        'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                                        isActive
                                            ? 'bg-primary-700 text-white'
                                            : 'text-primary-300 hover:bg-primary-800 hover:text-white'
                                    )
                                }
                            >
                                <item.icon className="w-5 h-5" />
                                <span className="font-medium">{item.label}</span>
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* Footer */}
            <div className="p-6 border-t border-primary-800">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-primary-700 flex items-center justify-center font-semibold">
                        А
                    </div>
                    <div>
                        <p className="font-medium">Арман</p>
                        <p className="text-xs text-primary-300">Администратор</p>
                    </div>
                </div>
            </div>
        </aside>
    );
};
