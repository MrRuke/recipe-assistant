import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LanguageService } from '../../services/language.service';

@Component({
    selector: 'app-settings',
    imports: [FormsModule],
    templateUrl: './settings.component.html',
    styleUrl: './settings.component.css'
})
export class SettingsComponent implements OnInit {
    private langService = inject(LanguageService);

    protected height = signal<number | null>(null);
    protected weight = signal<number | null>(null);
    protected goal = signal<string>('maintain');
    protected saved = signal(false);

    protected heightValue: number | null = null;
    protected weightValue: number | null = null;
    protected goalValue: string = 'maintain';

    ngOnInit() {
        const savedSettings = localStorage.getItem('userSettings');
        if (savedSettings) {
            try {
                const settings = JSON.parse(savedSettings);
                this.heightValue = settings.height ?? null;
                this.weightValue = settings.weight ?? null;
                this.goalValue = settings.goal ?? 'maintain';
                this.height.set(this.heightValue);
                this.weight.set(this.weightValue);
                this.goal.set(this.goalValue);
            } catch {
                // ignore
            }
        }
    }

    protected translate(key: string): string {
        return this.langService.translate(key);
    }

    protected onSave() {
        const settings = {
            height: this.heightValue,
            weight: this.weightValue,
            goal: this.goalValue
        };
        localStorage.setItem('userSettings', JSON.stringify(settings));
        this.height.set(this.heightValue);
        this.weight.set(this.weightValue);
        this.goal.set(this.goalValue);
        this.saved.set(true);
        setTimeout(() => this.saved.set(false), 2500);
    }

    protected getBMI(): string | null {
        if (!this.heightValue || !this.weightValue || this.heightValue <= 0) return null;
        const heightM = this.heightValue / 100;
        const bmi = this.weightValue / (heightM * heightM);
        return bmi.toFixed(1);
    }

    protected getBMICategory(): string {
        const bmi = parseFloat(this.getBMI() ?? '0');
        if (!bmi) return '';
        const lang = this.langService.language();
        if (bmi < 18.5) return lang === 'ru' ? 'Недостаток веса' : 'Underweight';
        if (bmi < 25) return lang === 'ru' ? 'Норма' : 'Normal';
        if (bmi < 30) return lang === 'ru' ? 'Избыточный вес' : 'Overweight';
        return lang === 'ru' ? 'Ожирение' : 'Obese';
    }

    protected getBMIColor(): string {
        const bmi = parseFloat(this.getBMI() ?? '0');
        if (!bmi) return '';
        if (bmi < 18.5) return 'bmi-low';
        if (bmi < 25) return 'bmi-normal';
        if (bmi < 30) return 'bmi-high';
        return 'bmi-very-high';
    }
}
