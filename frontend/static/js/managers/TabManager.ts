// Tab functionality
export class TabManager {
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