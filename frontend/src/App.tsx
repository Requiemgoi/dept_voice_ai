import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { ClientsPage } from './pages/ClientsPage';
import { CallHistoryPage } from './pages/CallHistoryPage';
import { ReportsPage } from './pages/ReportsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';
import { Toaster } from 'react-hot-toast';

function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen">
                <Toaster position="top-right" />
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/clients" element={<ClientsPage />} />
                    <Route path="/history" element={<CallHistoryPage />} />
                    <Route path="/reports" element={<ReportsPage />} />
                    <Route path="/analytics" element={<AnalyticsPage />} />
                    <Route path="/settings" element={<SettingsPage />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </div>
        </BrowserRouter>
    );
}

export default App;
