import React, { useState, useEffect } from 'react';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';
import type { Settings, Language, Theme } from '../../types/settings';

interface SettingsModalProps {
    isOpen: boolean;
    onClose: () => void;
    settings: Settings;
    onSave: (settings: Settings) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
    isOpen,
    onClose,
    settings,
    onSave,
}) => {
    const [formData, setFormData] = useState<Settings>(settings);
    const [errors, setErrors] = useState<Partial<Record<keyof Settings, string>>>({});

    useEffect(() => {
        setFormData(settings);
        setErrors({});
    }, [settings, isOpen]);

    const validateUrl = (url: string): boolean => {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const newErrors: Partial<Record<keyof Settings, string>> = {};

        if (!formData.apiUrl.trim()) {
            newErrors.apiUrl = 'API URL обязателен';
        } else if (!validateUrl(formData.apiUrl)) {
            newErrors.apiUrl = 'Некорректный URL';
        }

        if (formData.autoRefreshInterval < 0) {
            newErrors.autoRefreshInterval = 'Интервал не может быть отрицательным';
        }

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        onSave(formData);
        onClose();
    };

    const handleCancel = () => {
        setFormData(settings);
        setErrors({});
        onClose();
    };

    return (
        <Modal
            isOpen={isOpen}
            onClose={handleCancel}
            title="⚙️ Настройки"
            footer={
                <div className="flex justify-end gap-3">
                    <Button variant="secondary" onClick={handleCancel}>
                        Отмена
                    </Button>
                    <Button variant="primary" onClick={handleSubmit}>
                        Сохранить
                    </Button>
                </div>
            }
        >
            <form onSubmit={handleSubmit} className="space-y-4">
                {/* API URL */}
                <div>
                    <label htmlFor="apiUrl" className="block text-sm font-medium text-gray-300 mb-1">
                        API URL
                    </label>
                    <input
                        type="text"
                        id="apiUrl"
                        value={formData.apiUrl}
                        onChange={(e) => setFormData({ ...formData, apiUrl: e.target.value })}
                        className="w-full px-3 py-2 bg-black/20 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
                        placeholder="http://localhost:8000"
                    />
                    {errors.apiUrl && (
                        <p className="text-sm text-red-400 mt-1">{errors.apiUrl}</p>
                    )}
                </div>

                {/* Language */}
                <div>
                    <label htmlFor="language" className="block text-sm font-medium text-gray-300 mb-1">
                        Язык интерфейса
                    </label>
                    <select
                        id="language"
                        value={formData.language}
                        onChange={(e) => setFormData({ ...formData, language: e.target.value as Language })}
                        className="w-full px-3 py-2 bg-black/20 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all appearance-none"
                    >
                        <option value="ru" className="bg-gray-900 text-white">Русский</option>
                        <option value="en" className="bg-gray-900 text-white">English</option>
                        <option value="kk" className="bg-gray-900 text-white">Қазақша</option>
                    </select>
                </div>

                {/* Demo Mode */}
                <div className="flex items-center p-3 rounded-lg border border-white/10 bg-white/5">
                    <input
                        type="checkbox"
                        id="demoMode"
                        checked={formData.demoMode}
                        onChange={(e) => setFormData({ ...formData, demoMode: e.target.checked })}
                        className="w-4 h-4 text-purple-600 rounded focus:ring-purple-500 bg-black/20 border-white/10"
                    />
                    <label htmlFor="demoMode" className="ml-2 text-sm text-gray-300 cursor-pointer select-none">
                        Демо режим <span className="text-gray-500">(использовать тестовые звонки)</span>
                    </label>
                </div>

                {/* Auto Refresh Interval */}
                <div>
                    <label htmlFor="autoRefreshInterval" className="block text-sm font-medium text-gray-300 mb-1">
                        Автообновление данных (сек)
                    </label>
                    <input
                        type="number"
                        id="autoRefreshInterval"
                        value={formData.autoRefreshInterval}
                        onChange={(e) => setFormData({ ...formData, autoRefreshInterval: parseInt(e.target.value) || 0 })}
                        className="w-full px-3 py-2 bg-black/20 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
                        min="0"
                        step="1"
                    />
                    {errors.autoRefreshInterval && (
                        <p className="text-sm text-red-400 mt-1">{errors.autoRefreshInterval}</p>
                    )}
                </div>
            </form>
        </Modal>
    );
};
