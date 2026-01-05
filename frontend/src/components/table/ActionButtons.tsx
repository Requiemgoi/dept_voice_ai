import React from 'react';
import { Play, Eye } from 'lucide-react';
import { Button } from '../ui/Button';
import type { Client } from '../../types/client';

interface ActionButtonsProps {
    client: Client;
    onProcess: (id: number) => void;
    onViewDetails: (client: Client) => void;
    isProcessing: boolean;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({
    client,
    onProcess,
    onViewDetails,
    isProcessing,
}) => {
    const canProcess = client.status === 'pending' || client.status === 'failed';

    return (
        <div className="flex items-center gap-2">
            <Button
                size="sm"
                variant="primary"
                onClick={() => onProcess(client.id)}
                disabled={!canProcess || isProcessing}
                isLoading={isProcessing && client.status === 'processing'}
                title="Начать обработку"
            >
                <Play className="w-4 h-4" />
            </Button>

            <Button
                size="sm"
                variant="secondary"
                onClick={() => onViewDetails(client)}
                title="Просмотр деталей"
            >
                <Eye className="w-4 h-4" />
            </Button>
        </div>
    );
};
