import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ToastComponent } from './components/toast.component/toast.component';
import { LanguageService } from './services/language.service';

@Component({
    selector: 'app-root',
    imports: [RouterModule, ToastComponent],
    templateUrl: './app.html',
    styleUrl: './app.css'
})
export class App implements OnInit {
    private langService = inject(LanguageService);

    protected isDark = signal(false);
    protected lang = this.langService.language;

    ngOnInit() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            this.setTheme(true);
        } else {
            this.setTheme(false); // Default to light
        }
    }

    protected toggleTheme() {
        this.setTheme(!this.isDark());
    }

    protected setLanguage(event: Event) {
        const select = event.target as HTMLSelectElement;
        this.langService.setLanguage(select.value as 'en' | 'ru');
    }

    protected translate(key: string): string {
        return this.langService.translate(key);
    }

    private setTheme(dark: boolean) {
        this.isDark.set(dark);
        const body = document.body;
        if (dark) {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    }
}
