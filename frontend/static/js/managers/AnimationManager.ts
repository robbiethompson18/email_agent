// Animation manager
export class AnimationManager {
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