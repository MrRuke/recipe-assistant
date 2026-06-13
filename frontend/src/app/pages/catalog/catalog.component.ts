import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { RecipeService, Test } from '../../api/api.service';
import { LanguageService } from '../../services/language.service';
import { ToastService } from '../../services/toast.service';

@Component({
    selector: 'app-catalog',
    templateUrl: './catalog.component.html',
    styleUrl: './catalog.component.css',
})
export class CatalogComponent {
    private recipeService = inject(RecipeService);
    private router = inject(Router);
    private langService = inject(LanguageService);
    private toastService = inject(ToastService);

    protected catalog = signal<Test[]>([]);

    ngOnInit() {
        this.loadCatalog();
    }

    loadCatalog() {
        this.recipeService.getCatalog().subscribe({
            next: (res) => this.catalog.set(res.catalog),
            error: (err) => {
                console.error('Error:', err);
                this.toastService.show(this.translate('catalog.toast.error'), 'error');
            }
        });
    }

    selectRecipe(recipeName: string) {
        this.router.navigate(['/'], { queryParams: { q: recipeName } });
    }

    protected translate(key: string): string {
        return this.langService.translate(key);
    }
}
