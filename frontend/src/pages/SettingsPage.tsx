import React, { useState } from 'react';
import { MainLayout } from '../components/layout/MainLayout';
import { useSettings } from '../hooks/useSettings';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Switch, TextField, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { Save, RotateCcw, Server, Beaker } from 'lucide-react';
import toast from 'react-hot-toast';

export const SettingsPage: React.FC = () => {
    const { settings, updateSettings, resetSettings } = useSettings();
    const [localSettings, setLocalSettings] = useState(settings);

    const handleSave = () => {
        updateSettings(localSettings);
        toast.success('Настройки сохранены');
    };

    const handleReset = () => {
        resetSettings();
        setLocalSettings(settings);
        toast.success('Настройки сброшены');
    };

    return (
        <MainLayout>
            <div className="p-8 max-w-4xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Настройки</h1>
                    <p className="text-gray-500 mt-1">Конфигурация параметров системы</p>
                </div>

                <div className="space-y-6">
                    {/* General Settings */}
                    <Card title="Общие настройки">
                        <div className="space-y-6">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <Beaker className="w-5 h-5 text-gray-400" />
                                    <div>
                                        <p className="font-medium">Демо-режим</p>
                                        <p className="text-sm text-gray-500">Использовать случайные ответы вместо реальных</p>
                                    </div>
                                </div>
                                <Switch
                                    checked={localSettings.demoMode}
                                    onChange={(e) => setLocalSettings({ ...localSettings, demoMode: e.target.checked })}
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <FormControl fullWidth size="small">
                                    <InputLabel>Язык интерфейса</InputLabel>
                                    <Select
                                        value={localSettings.language}
                                        label="Язык интерфейса"
                                        onChange={(e) => setLocalSettings({ ...localSettings, language: e.target.value as any })}
                                    >
                                        <MenuItem value="ru">Русский</MenuItem>
                                        <MenuItem value="kk">Қазақша</MenuItem>
                                        <MenuItem value="en">English</MenuItem>
                                    </Select>
                                </FormControl>
                            </div>
                        </div>
                    </Card>

                    {/* API Settings */}
                    <Card title="Настройки API">
                        <div className="space-y-4">
                            <div className="flex items-center gap-3 mb-2">
                                <Server className="w-5 h-5 text-gray-400" />
                                <p className="font-medium">Backend Server</p>
                            </div>
                            <TextField
                                fullWidth
                                label="API URL"
                                size="small"
                                value={localSettings.apiUrl}
                                onChange={(e) => setLocalSettings({ ...localSettings, apiUrl: e.target.value })}
                                helperText="Адрес сервера backend (например, http://localhost:8000)"
                            />
                        </div>
                    </Card>

                    {/* Action Buttons */}
                    <div className="flex items-center justify-end gap-3 pt-4">
                        <Button
                            variant="secondary"
                            onClick={handleReset}
                        >
                            <RotateCcw className="w-4 h-4 mr-2" />
                            Сбросить
                        </Button>
                        <Button
                            variant="primary"
                            onClick={handleSave}
                        >
                            <Save className="w-4 h-4 mr-2" />
                            Сохранить изменения
                        </Button>
                    </div>
                </div>
            </div>
        </MainLayout>
    );
};
