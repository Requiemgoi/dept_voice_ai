import React from 'react';
import clsx from 'clsx';

interface CardProps {
    children: React.ReactNode;
    title?: string;
    className?: string;
    onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, title, className, onClick }) => {
    return (
        <div
            className={clsx(
                'card bg-white rounded-lg shadow-sm border border-gray-200 p-6',
                onClick && 'cursor-pointer hover:shadow-md transition-shadow',
                className
            )}
            onClick={onClick}
        >
            {title && <h3 className="text-lg font-semibold mb-4 text-gray-900">{title}</h3>}
            {children}
        </div>
    );
};
