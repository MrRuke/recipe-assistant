import { Component, input } from '@angular/core';
import { Recipe } from '../../api/models/all.i';

@Component({
    selector: 'app-card',
    imports: [],
    templateUrl: './card.component.html',
    styleUrl: './card.component.css',
})
export class CardComponent {
    public recipe = input.required<Recipe>();
}
