import { Component, inject, signal } from '@angular/core';
import { RecipeService, Test } from '../../api/api.service';

@Component({
    selector: 'app-catalog',
    templateUrl: './catalog.component.html',
    styleUrl: './catalog.component.css',
})
export class CatalogComponent {
    private recipeService = inject(RecipeService);

    protected catalog = signal<Test[]>([]);

    ngOnInit() {
        this.loadCatalog();
    }

    loadCatalog() {
        this.recipeService.getCatalog().subscribe({
            next: (res) => this.catalog.set(res.catalog),
            error: (err) => console.error('Error:', err)
        });
    }
}
