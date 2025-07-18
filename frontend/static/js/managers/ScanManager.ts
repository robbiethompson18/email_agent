import { EmailCandidate } from '../types.js';
import { EmailRenderer } from '../components/email_renderer.js';

// Scan button functionality
export class ScanManager {
    private scanButton: HTMLButtonElement | null;
    private emailRenderer: EmailRenderer;

    constructor(emailRenderer: EmailRenderer) {
        this.emailRenderer = emailRenderer;
        this.scanButton = document.querySelector<HTMLButtonElement>('.primary-button');
        this.init();
    }

    private init(): void {
        this.attachScanButtonListener();
    }

    private attachScanButtonListener(): void {
        // Use event delegation to handle dynamically created scan buttons
        document.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            if (target.classList.contains('primary-button')) {
                this.handleScanClick();
            }
        });
    }

    private async handleScanClick(): Promise<void> {
        const scanButton = document.querySelector<HTMLButtonElement>('.primary-button');
        if (!scanButton) return;

        // Update button state
        scanButton.textContent = 'Scanning...';
        scanButton.disabled = true;
        
        try {
            console.log("calling API...")
            const response = await fetch('http://localhost:8000/emails/candidates');
            console.log("response:", response)
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            
            const candidates = await response.json();
            console.log('received candidates:', candidates)
            
            // Display candidates using the email renderer
            this.displayCandidates(candidates);
            
        } catch (error) {
            console.error('Scan failed:', error);
        } finally {
            // Reset button state
            scanButton.textContent = 'Scan for Emails';
            scanButton.disabled = false;
        }
    }

    private displayCandidates(candidates: EmailCandidate[]): void {
        this.emailRenderer.renderEmailList('candidates', candidates, {
            showActions: true,
            actionType: 'candidate',
            onUnsubscribe: (emailId: string) => {
                console.log(`Unsubscribing from email: ${emailId}`);
                // TODO: Implement actual unsubscribe logic
            },
            onSkip: (emailId: string) => {
                console.log(`Skipping email: ${emailId}`);
                // TODO: Implement actual skip logic
            }
        });
    }
}