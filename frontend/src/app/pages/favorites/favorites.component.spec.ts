import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FavoritesComponent } from './favorites.component';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';

describe('FavoritesComponent', () => {
    let component: FavoritesComponent;
    let fixture: ComponentFixture<FavoritesComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [FavoritesComponent],
            providers: [
                provideHttpClient(),
                provideRouter([])
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(FavoritesComponent);
        component = fixture.componentInstance;
        await fixture.whenStable();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
