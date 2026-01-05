import React from 'react';
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './Button';

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
    footer?: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({
    isOpen,
    onClose,
    title,
    children,
    footer,
}) => {
    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black bg-opacity-50 z-40"
                        onClick={onClose}
                    />

                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 20 }}
                        transition={{ duration: 0.2 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-4"
                    >
                        <div className="glass-strong rounded-xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-hidden flex flex-col border border-purple-500/30">
                            {/* Header */}
                            <div className="flex items-center justify-between px-6 py-4 border-b border-white/10">
                                <h2 className="text-xl font-bold bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">{title}</h2>
                                <button
                                    onClick={onClose}
                                    className="text-gray-400 hover:text-white transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            {/* Content */}
                            <div className="flex-1 overflow-y-auto px-6 py-4 scrollbar-thin scrollbar-thumb-purple-500/20 scrollbar-track-transparent">
                                {children}
                            </div>

                            {/* Footer */}
                            {footer && (
                                <div className="px-6 py-4 border-t border-white/10 bg-black/20">
                                    {footer}
                                </div>
                            )}
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};
