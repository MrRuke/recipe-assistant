import { ComponentFixture, TestBed } from '@angular/core/testing';
import { GeneratorComponent } from './generator.component';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';

describe('GeneratorComponent', () => {
    let component: GeneratorComponent;
    let fixture: ComponentFixture<GeneratorComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [GeneratorComponent],
            providers: [
                provideHttpClient(),
                provideRouter([])
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(GeneratorComponent);
        component = fixture.componentInstance;
        await fixture.whenStable();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
