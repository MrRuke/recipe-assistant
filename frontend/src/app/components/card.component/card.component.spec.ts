import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CardComponent } from './card.component';

describe('CardComponent', () => {
    let component: CardComponent;
    let fixture: ComponentFixture<CardComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [CardComponent],
        }).compileComponents();

        fixture = TestBed.createComponent(CardComponent);
        component = fixture.componentInstance;
        fixture.componentRef.setInput('recipe', {
            title: 'Test Recipe',
            description: 'Test Description',
            macros: {
                calories: 300,
                protein_g: 20,
                fat_g: 10,
                carbs_g: 30
            },
            prep_time_minutes: 20,
            ingredients: [
                { name: 'Ingredient 1', amount: '100g' }
            ],
            steps: ['Step 1'],
            substitutions: []
        });
        await fixture.whenStable();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
