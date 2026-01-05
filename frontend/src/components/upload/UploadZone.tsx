import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, FileSpreadsheet, Loader2 } from 'lucide-react';
import { ACCEPTED_FILE_TYPES, MAX_FILE_SIZE } from '../../utils/constants';
import toast from 'react-hot-toast';

interface UploadZoneProps {
    onUpload: (file: File) => void;
    isUploading: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onUpload, isUploading }) => {
    const onDrop = useCallback(
        (acceptedFiles: File[]) => {
            if (acceptedFiles.length === 0) {
                return;
            }

            const file = acceptedFiles[0];

            if (file.size > MAX_FILE_SIZE) {
                toast.error('Файл слишком большой. Максимальный размер: 10 МБ');
                return;
            }

            onUpload(file);
        },
        [onUpload]
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: ACCEPTED_FILE_TYPES,
        maxFiles: 1,
        disabled: isUploading,
    });

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="w-full"
        >
            <div
                {...getRootProps()}
                className={`
        cursor-pointer transition-all duration-300 p-12 rounded-xl
        border-2 border-dashed
        ${isDragActive
                        ? 'glass-strong border-cyan-500 shadow-[0_0_30px_rgba(34,211,238,0.2)]'
                        : 'glass border-white/10 hover:border-purple-500/50 hover:bg-white/5'}
        ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
            >
                <input {...getInputProps()} />

                <div className="flex flex-col items-center justify-center text-center">
                    {isUploading ? (
                        <>
                            <Loader2 className="w-16 h-16 text-cyan-400 animate-spin mb-4" />
                            <p className="text-lg font-medium text-white mb-2">
                                Загрузка файла...
                            </p>
                            <p className="text-sm text-gray-400">
                                Пожалуйста, подождите
                            </p>
                        </>
                    ) : isDragActive ? (
                        <>
                            <Upload className="w-16 h-16 text-cyan-400 mb-4 animate-bounce" />
                            <p className="text-lg font-medium text-white mb-2">
                                Отпустите файл для загрузки
                            </p>
                        </>
                    ) : (
                        <>
                            <div className="p-4 rounded-full bg-white/5 mb-4 group-hover:scale-110 transition-transform duration-300">
                                <FileSpreadsheet className="w-12 h-12 text-purple-400" />
                            </div>
                            <p className="text-lg font-medium text-white mb-2">
                                Перетащите Excel файл сюда
                            </p>
                            <p className="text-sm text-gray-400 mb-4">
                                или нажмите, чтобы выбрать файл
                            </p>
                            <p className="text-xs text-gray-500">
                                Поддерживаются форматы: .xlsx, .xls (макс. 10 МБ)
                            </p>
                        </>
                    )}
                </div>
            </div>

            <div className="mt-6 glass p-4 rounded-lg border border-white/10">
                <h3 className="text-sm font-semibold text-cyan-400 mb-2">
                    Требования к Excel файлу:
                </h3>
                <ul className="text-sm text-gray-400 space-y-1">
                    <li>• <strong>Номер телефона</strong> (международный формат)</li>
                    <li>• <strong>ФИО клиента</strong></li>
                    <li>• <strong>ИИН</strong></li>
                    <li>• <strong>Кредитор</strong></li>
                    <li>• <strong>Сумма долга</strong></li>
                    <li>• <strong>Дни просрочки</strong></li>
                </ul>
            </div>
        </motion.div>
    );
};
