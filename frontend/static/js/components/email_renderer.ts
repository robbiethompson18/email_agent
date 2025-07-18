import { EmailCandidate, EmailRenderOptions } from '../types.js';

// Email renderer for displaying different types of emails
export class EmailRenderer {
    
    renderEmailList(
        containerId: string, 
        emails: EmailCandidate[], 
        options: EmailRenderOptions = {}
    ): void {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Clear existing content
        container.innerHTML = '';

        // Create header
        const header = this.createHeader(emails.length, options);
        container.appendChild(header);

        // Create emails list
        const emailsList = this.createEmailsList(emails, options);
        container.appendChild(emailsList);

        // Attach event listeners if actions are enabled
        if (options.showActions) {
            this.attachActionListeners(options);
        }
    }

    private createHeader(emailCount: number, options: EmailRenderOptions): HTMLElement {
        const header = document.createElement('div');
        header.className = 'content-header';
        
        const title = this.getHeaderTitle(options.actionType, emailCount);
        let headerHTML = `<h2>${title}</h2>`;
        
        // Add scan button only for candidates
        if (options.actionType === 'candidate') {
            headerHTML += `<button class="primary-button">Scan for Emails</button>`;
        }
        
        header.innerHTML = headerHTML;
        return header;
    }

    private getHeaderTitle(actionType: string | undefined, count: number): string {
        switch (actionType) {
            case 'candidate':
                return `Email Candidates (${count})`;
            case 'unsubscribed':
                return `Unsubscribed Emails (${count})`;
            case 'skipped':
                return `Skipped Emails (${count})`;
            default:
                return `Emails (${count})`;
        }
    }

    private createEmailsList(emails: EmailCandidate[], options: EmailRenderOptions): HTMLElement {
        const emailsList = document.createElement('div');
        emailsList.className = 'emails-list';

        emails.forEach(email => {
            const emailCard = this.createEmailCard(email, options);
            emailsList.appendChild(emailCard);
        });

        return emailsList;
    }

    private createEmailCard(email: EmailCandidate, options: EmailRenderOptions): HTMLElement {
        const emailCard = document.createElement('div');
        emailCard.className = 'email-card';
        
        let cardHTML = `
            <div class="email-header">
                <h3>${email.subject}</h3>
                <span class="email-date">${email.date}</span>
            </div>
            <p class="email-sender">From: ${email.sender}</p>
        `;

        // Add actions based on email type
        if (options.showActions) {
            cardHTML += this.createActionsHTML(email.id, options.actionType);
        }

        emailCard.innerHTML = cardHTML;
        return emailCard;
    }

    private createActionsHTML(emailId: string, actionType: string | undefined): string {
        switch (actionType) {
            case 'candidate':
                return `
                    <div class="email-actions">
                        <button class="action-button unsubscribe-btn" data-id="${emailId}">
                            Unsubscribe
                        </button>
                        <button class="action-button skip-btn" data-id="${emailId}">
                            Skip
                        </button>
                    </div>
                `;
            case 'unsubscribed':
                return `
                    <div class="email-actions">
                        <span class="status-indicator success">✓ Unsubscribed</span>
                    </div>
                `;
            case 'skipped':
                return `
                    <div class="email-actions">
                        <span class="status-indicator skipped">⊝ Skipped</span>
                        <button class="action-button unsubscribe-btn" data-id="${emailId}">
                            Unsubscribe
                        </button>
                    </div>
                `;
            default:
                return '';
        }
    }

    private attachActionListeners(options: EmailRenderOptions): void {
        // Add event listeners for unsubscribe buttons
        const unsubscribeButtons = document.querySelectorAll('.unsubscribe-btn');
        unsubscribeButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const emailId = (e.target as HTMLElement).getAttribute('data-id');
                if (emailId && options.onUnsubscribe) {
                    options.onUnsubscribe(emailId);
                }
            });
        });

        // Add event listeners for skip buttons
        const skipButtons = document.querySelectorAll('.skip-btn');
        skipButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const emailId = (e.target as HTMLElement).getAttribute('data-id');
                if (emailId && options.onSkip) {
                    options.onSkip(emailId);
                }
            });
        });
    }
}