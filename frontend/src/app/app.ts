import { Component, OnInit, signal } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-root',
    imports: [RouterModule],
    templateUrl: './app.html',
    styleUrl: './app.css'
})
export class App implements OnInit {
    protected isDark = signal(false);

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
