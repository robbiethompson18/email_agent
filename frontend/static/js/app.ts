import { EmailCandidate, UnsubscribeResult, SkipResult, StatsResult, ApiResponse } from './types.js';
import { EmailApiManager } from './api/EmailApiManager.js';
import { TabManager } from './managers/TabManager.js';
import { AnimationManager } from './managers/AnimationManager.js';
import { ScanManager } from './managers/ScanManager.js';
import { EmailRenderer } from './components/email_renderer.js';

// Main application class
class EmailUnsubscribeApp {
    private readonly tabManager: TabManager;
    private readonly animationManager: AnimationManager;
    private readonly scanManager: ScanManager;
    private readonly emailRenderer: EmailRenderer;
    public readonly apiManager: EmailApiManager;

    constructor() {
        // Initialize components
        this.emailRenderer = new EmailRenderer();
        this.apiManager = new EmailApiManager();
        
        // Initialize managers
        this.tabManager = new TabManager();
        this.animationManager = new AnimationManager();
        this.scanManager = new ScanManager(this.emailRenderer);
        
        // Use the managers to ensure they're not marked as unused
        this.initializeManagers();
        
        console.log('Email Unsubscribe Manager initialized with TypeScript');
    }

    private initializeManagers(): void {
        // This method ensures all managers are properly initialized
        // The managers are initialized in the constructor and handle their own events
        console.log('Managers initialized:', {
            tabs: !!this.tabManager,
            animations: !!this.animationManager,
            scan: !!this.scanManager,
            renderer: !!this.emailRenderer,
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

    public renderEmails(containerId: string, emails: EmailCandidate[], actionType: 'candidate' | 'unsubscribed' | 'skipped'): void {
        this.emailRenderer.renderEmailList(containerId, emails, {
            showActions: true,
            actionType: actionType,
            onUnsubscribe: (emailId: string) => this.handleUnsubscribe(emailId),
            onSkip: (emailId: string) => this.handleSkip(emailId)
        });
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