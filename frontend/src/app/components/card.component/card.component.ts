import { Component, inject, input } from '@angular/core';
import { Recipe } from '../../api/models/all.i';
import { LanguageService } from '../../services/language.service';

@Component({
    selector: 'app-card',
    imports: [],
    templateUrl: './card.component.html',
    styleUrl: './card.component.css',
})
export class CardComponent {
    private langService = inject(LanguageService);

    public recipe = input.required<Recipe>();

    protected translate(key: string): string {
        return this.langService.translate(key);
    }
}
