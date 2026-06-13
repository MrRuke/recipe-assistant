import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LanguageService } from '../../services/language.service';
import { RecipeService } from '../../api/api.service';
import { ToastService } from '../../services/toast.service';

@Component({
    selector: 'app-settings',
    imports: [FormsModule],
    templateUrl: './settings.component.html',
    styleUrl: './settings.component.css'
})
export class SettingsComponent implements OnInit {
    private langService = inject(LanguageService);
    private recipeService = inject(RecipeService);
    private toastService = inject(ToastService);

    protected loading = signal(true);
    protected saving = signal(false);
    protected saved = signal(false);

    protected heightValue: number | null = null;
    protected weightValue: number | null = null;
    protected goalValue: string = 'maintain';

    ngOnInit() {
        this.loadSettings();
    }

    private loadSettings() {
        this.loading.set(true);
        this.recipeService.getSettings().subscribe({
            next: (settings) => {
                this.heightValue = settings.height_cm;
                this.weightValue = settings.weight_kg;
                this.goalValue = settings.goal ?? 'maintain';
                this.loading.set(false);
            },
            error: () => {
                // Fallback to localStorage if API fails
                const cached = localStorage.getItem('userSettings');
                if (cached) {
                    try {
                        const s = JSON.parse(cached);
                        this.heightValue = s.height ?? null;
                        this.weightValue = s.weight ?? null;
                        this.goalValue = s.goal ?? 'maintain';
                    } catch { /* ignore */ }
                }
                this.loading.set(false);
                this.toastService.show(this.translate('settings.toast.load.error'), 'error');
            }
        });
    }

    protected translate(key: string): string {
        return this.langService.translate(key);
    }

    protected onSave() {
        if (this.saving()) return;
        this.saving.set(true);

        const settings = {
            height_cm: this.heightValue,
            weight_kg: this.weightValue,
            goal: this.goalValue
        };

        this.recipeService.saveSettings(settings).subscribe({
            next: () => {
                // Also persist locally as a fast cache
                localStorage.setItem('userSettings', JSON.stringify({
                    height: this.heightValue,
                    weight: this.weightValue,
                    goal: this.goalValue
                }));
                this.saving.set(false);
                this.saved.set(true);
                this.toastService.show(this.translate('settings.toast.save.success'), 'success');
                setTimeout(() => this.saved.set(false), 2500);
            },
            error: () => {
                this.saving.set(false);
                this.toastService.show(this.translate('settings.toast.save.error'), 'error');
            }
        });
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
