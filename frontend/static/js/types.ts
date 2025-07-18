// TypeScript interfaces for email data
export interface EmailCandidate {
    id: string;
    sender: string;
    subject: string;
    body: string;
    date: string;
}

export interface UnsubscribeResult {
    success: boolean;
    message: string;
    method_used?: string;
}

export interface SkipResult {
    status: string;
}

export interface StatsResult {
    total_analyzed: number;
    unsubscribed: number;
    skipped: number;
}

export interface ApiResponse<T> {
    data?: T;
    error?: string;
}

export interface EmailRenderOptions {
    showActions?: boolean;
    actionType?: 'candidate' | 'unsubscribed' | 'skipped';
    onUnsubscribe?: (emailId: string) => void;
    onSkip?: (emailId: string) => void;
}