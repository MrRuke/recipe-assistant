import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { RecipeService, Test } from '../../api/api.service';

@Component({
    selector: 'app-catalog',
    templateUrl: './catalog.component.html',
    styleUrl: './catalog.component.css',
})
export class CatalogComponent {
    private recipeService = inject(RecipeService);
    private router = inject(Router);

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

    selectRecipe(recipeName: string) {
        this.router.navigate(['/'], { queryParams: { q: recipeName } });
    }
}
