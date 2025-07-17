// TypeScript interfaces for email data
interface EmailCandidate {
    id: string;
    sender: string;
    subject: string;
    body: string;
    date: string;
}

interface UnsubscribeResult {
    success: boolean;
    message: string;
    method_used?: string;
}

interface SkipResult {
    status: string;
}

interface StatsResult {
    total_analyzed: number;
    unsubscribed: number;
    skipped: number;
}

interface ApiResponse<T> {
    data?: T;
    error?: string;
}

// Tab functionality
class TabManager {
    private tabButtons: NodeListOf<HTMLElement>;
    private tabContents: NodeListOf<HTMLElement>;

    constructor() {
        this.tabButtons = document.querySelectorAll<HTMLElement>('.tab-button');
        this.tabContents = document.querySelectorAll<HTMLElement>('.tab-content');
        this.init();
    }

    private init(): void {
        this.tabButtons.forEach((button: HTMLElement) => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                if (targetTab) {
                    this.switchTab(targetTab, button);
                }
            });
        });
    }

    private switchTab(targetTab: string, clickedButton: HTMLElement): void {
        // Remove active class from all buttons and contents
        this.tabButtons.forEach((btn: HTMLElement) => btn.classList.remove('active'));
        this.tabContents.forEach((content: HTMLElement) => content.classList.remove('active'));

        // Add active class to clicked button and corresponding content
        clickedButton.classList.add('active');
        const targetContent = document.getElementById(targetTab);
        if (targetContent) {
            targetContent.classList.add('active');
        }
    }
}

// Scan button functionality
class ScanButtonManager {
    private scanButton: HTMLButtonElement | null;

    constructor() {
        this.scanButton = document.querySelector<HTMLButtonElement>('.primary-button');
        this.init();
    }

    private init(): void {
        if (this.scanButton) {
            this.scanButton.addEventListener('click', () => this.handleScanClick());
        }
    }

    private async handleScanClick(): Promise<void> {
        if (!this.scanButton) return;

        // Update button state
        this.scanButton.textContent = 'Scanning...';
        this.scanButton.disabled = true;
        
        try {
            // Simulate scanning process
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // You could call actual scan API here
            // const candidates = await emailManager.fetchCandidates();
            
            console.log('Scan completed (placeholder)');
        } catch (error) {
            console.error('Scan failed:', error);
        } finally {
            // Reset button state
            this.scanButton.textContent = 'Scan for Emails';
            this.scanButton.disabled = false;
        }
    }
}

// Animation manager
class AnimationManager {
    constructor() {
        this.init();
    }

    private init(): void {
        this.addSmoothScrollBehavior();
        this.addHoverEffects();
    }

    private addSmoothScrollBehavior(): void {
        document.documentElement.style.scrollBehavior = 'smooth';
    }

    private addHoverEffects(): void {
        const tabButtons = document.querySelectorAll<HTMLElement>('.tab-button');
        
        tabButtons.forEach((button: HTMLElement) => {
            button.addEventListener('mouseenter', () => {
                if (!button.classList.contains('active')) {
                    button.style.transform = 'translateY(-1px)';
                }
            });
            
            button.addEventListener('mouseleave', () => {
                if (!button.classList.contains('active')) {
                    button.style.transform = 'translateY(0)';
                }
            });
        });
    }
}

// API manager for backend communication
class EmailApiManager {
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

// Main application class
class EmailUnsubscribeApp {
    private readonly tabManager: TabManager;
    private readonly scanButtonManager: ScanButtonManager;
    private readonly animationManager: AnimationManager;
    public readonly apiManager: EmailApiManager;

    constructor() {
        this.tabManager = new TabManager();
        this.scanButtonManager = new ScanButtonManager();
        this.animationManager = new AnimationManager();
        this.apiManager = new EmailApiManager();
        
        // Use the managers to ensure they're not marked as unused
        this.initializeManagers();
        
        console.log('Email Unsubscribe Manager initialized with TypeScript');
    }

    private initializeManagers(): void {
        // This method ensures all managers are properly initialized
        // The managers are initialized in the constructor and handle their own events
        console.log('Managers initialized:', {
            tabs: !!this.tabManager,
            scan: !!this.scanButtonManager,
            animations: !!this.animationManager,
            api: !!this.apiManager
        });
    }

    // Public methods for external access
    public async loadCandidates(): Promise<EmailCandidate[]> {
        return await this.apiManager.fetchCandidates();
    }

    public async loadUnsubscribed(): Promise<EmailCandidate[]> {
        return await this.apiManager.fetchUnsubscribed();
    }

    public async handleUnsubscribe(emailId: string): Promise<UnsubscribeResult> {
        return await this.apiManager.unsubscribeEmail(emailId);
    }

    public async handleSkip(emailId: string): Promise<SkipResult> {
        return await this.apiManager.skipEmail(emailId);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', (): void => {
    const app = new EmailUnsubscribeApp();
    
    // Make app globally accessible for debugging/external access
    (window as any).emailApp = app;
});

// Export types for external use
export type {
    EmailCandidate,
    UnsubscribeResult,
    SkipResult,
    StatsResult,
    ApiResponse
};