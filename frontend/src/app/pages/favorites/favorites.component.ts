import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RecipeService } from '../../api/api.service';
import { Recipe, SavedRecipe } from '../../api/models/all.i';
import { CardComponent } from '../../components/card.component/card.component';

@Component({
    selector: 'app-favorites',
    imports: [
        CommonModule,
        FormsModule,

        CardComponent,
    ],
    templateUrl: './favorites.component.html',
    styleUrl: './favorites.component.css',
})
export class FavoritesComponent {
    private recipeService = inject(RecipeService);
    private cdr = inject(ChangeDetectorRef);

    favorites: SavedRecipe[] = [];
    selectedFavorite: Recipe | null = null;

    ngOnInit() {
        this.loadFavorites();
    }

    protected loadFavorites(): void {
        this.recipeService.getFavorites().subscribe({
            next: (res) => {
                this.favorites = res.favorites;
                console.log('res', res.favorites);
                this.cdr.detectChanges();
            },
            error: (err) => console.error(err)
        });
    }

    protected viewFavoriteDetails(recipeData: Recipe): void {
        this.selectedFavorite = recipeData;
    }

    protected closeFavoriteDetails(): void {
        this.selectedFavorite = null;
    }
}
