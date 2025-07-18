import { EmailCandidate, UnsubscribeResult, SkipResult, StatsResult } from '../types.js';

// API manager for backend communication
export class EmailApiManager {
    private readonly baseUrl: string = '/api';

    async fetchCandidates(): Promise<EmailCandidate[]> {
        try {
            const response = await fetch(`${this.baseUrl}/emails/candidates`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const candidates: EmailCandidate[] = await response.json();
            return candidates;
        } catch (error) {
            console.error('Error fetching candidates:', error);
            return [];
        }
    }

    async fetchUnsubscribed(): Promise<EmailCandidate[]> {
        try {
            const response = await fetch(`${this.baseUrl}/emails/unsubscribed`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const unsubscribed: EmailCandidate[] = await response.json();
            return unsubscribed;
        } catch (error) {
            console.error('Error fetching unsubscribed emails:', error);
            return [];
        }
    }

    async unsubscribeEmail(emailId: string): Promise<UnsubscribeResult> {
        try {
            const response = await fetch(`${this.baseUrl}/emails/${emailId}/unsubscribe`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result: UnsubscribeResult = await response.json();
            return result;
        } catch (error) {
            console.error('Error unsubscribing:', error);
            return { 
                success: false, 
                message: error instanceof Error ? error.message : 'Network error' 
            };
        }
    }

    async skipEmail(emailId: string): Promise<SkipResult> {
        try {
            const response = await fetch(`${this.baseUrl}/emails/${emailId}/skip`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result: SkipResult = await response.json();
            return result;
        } catch (error) {
            console.error('Error skipping email:', error);
            return { status: 'error' };
        }
    }

    async getStats(): Promise<StatsResult> {
        try {
            const response = await fetch(`${this.baseUrl}/emails/stats`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const stats: StatsResult = await response.json();
            return stats;
        } catch (error) {
            console.error('Error fetching stats:', error);
            return { total_analyzed: 0, unsubscribed: 0, skipped: 0 };
        }
    }
}