import { ChangeDetectorRef, Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RecipeService } from '../../api/api.service';
import { Recipe } from '../../api/models/all.i';
import { CardComponent } from '../../components/card.component/card.component';
import { ToastService } from '../../services/toast.service';

@Component({
    selector: 'app-generator',
    imports: [
        FormsModule,
        CardComponent,
    ],
    templateUrl: './generator.component.html',
    styleUrl: './generator.component.css',
})
export class GeneratorComponent {
    private recipeService = inject(RecipeService);
    private cdr = inject(ChangeDetectorRef);

    protected isLoading = signal(false);
    protected isSaved = signal(false);

    protected currentRecipe = signal<Recipe | null>(null);

    protected searchQuery = signal('');
    protected refinementQuery= signal('');
    protected revisionsLeft = signal(2);

    private originalQuery = signal<string | undefined>(undefined);

    private toastService = inject(ToastService);

  protected generateRecipe(): void {
    if (!this.searchQuery().trim()) return;
    this.toastService.show('Generating recipe...');
    this.isLoading.set(true);
    this.currentRecipe.set(null);
    this.isSaved.set(false);
    this.revisionsLeft.set(2);
    this.originalQuery.set(this.searchQuery());

    this.recipeService.generateRecipe(this.searchQuery()).subscribe({
      next: (recipe) => {
        this.currentRecipe.set(recipe);
        this.isLoading.set(false);
        this.cdr.detectChanges();
        this.toastService.show('Recipe generated!');
      },
      error: (err) => {
        console.error('Error:', err);
        this.isLoading.set(false);
        this.toastService.show('Error generating recipe');
      }
    });
  }

    protected refineRecipe(): void {
        if (!this.refinementQuery().trim() || !this.currentRecipe() || this.revisionsLeft() <= 0) return;

        this.isLoading.set(true);
        this.recipeService.refineRecipe(this.currentRecipe()!, this.refinementQuery()).subscribe({
            next: (updatedRecipe) => {
                this.currentRecipe.set(updatedRecipe);
                this.revisionsLeft.set(this.revisionsLeft() - 1);
                this.refinementQuery.set('');
                this.isLoading.set(false);
            },
            error: (err) => {
                console.error('Error:', err);
                this.isLoading.set(false);
            }
        });
    }

    protected saveRecipe(): void {
        if (!this.currentRecipe()) return;

        this.recipeService.saveRecipe(this.originalQuery()!, this.currentRecipe()!).subscribe({
            next: () => {
                this.isSaved.set(true);
                alert('Saved!');
            },
            error: (err) => {
                console.error('Error:', err);
            }
        });
    }
}
