import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CatalogComponent } from './catalog.component';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';

describe('CatalogComponent', () => {
    let component: CatalogComponent;
    let fixture: ComponentFixture<CatalogComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [CatalogComponent],
            providers: [
                provideHttpClient(),
                provideRouter([])
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(CatalogComponent);
        component = fixture.componentInstance;
        await fixture.whenStable();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
