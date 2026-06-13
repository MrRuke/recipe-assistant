import { ChangeDetectorRef, Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { RecipeService } from '../../api/api.service';
import { Recipe } from '../../api/models/all.i';
import { CardComponent } from '../../components/card.component/card.component';
import { ToastService } from '../../services/toast.service';
import { LanguageService } from '../../services/language.service';

@Component({
    selector: 'app-generator',
    imports: [
        FormsModule,
        CardComponent,
    ],
    templateUrl: './generator.component.html',
    styleUrl: './generator.component.css',
})
export class GeneratorComponent implements OnInit {
    private recipeService = inject(RecipeService);
    private route = inject(ActivatedRoute);
    private cdr = inject(ChangeDetectorRef);
    private langService = inject(LanguageService);

    protected isLoading = signal(false);
    protected isSaved = signal(false);

    protected currentRecipe = signal<Recipe | null>(null);

    protected searchQuery = signal('');
    protected refinementQuery= signal('');
    protected revisionsLeft = signal(2);

    private originalQuery = signal<string | undefined>(undefined);

    private toastService = inject(ToastService);

    ngOnInit(): void {
        this.route.queryParams.subscribe(params => {
            const query = params['q'];
            if (query) {
                this.searchQuery.set(query);
            }
        });
    }

    protected translate(key: string): string {
        return this.langService.translate(key);
    }

  protected generateRecipe(): void {
    if (!this.searchQuery().trim()) return;
    this.toastService.show(this.translate('generator.toast.generating'));
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
        this.toastService.show(this.translate('generator.toast.success'));
      },
      error: (err) => {
        console.error('Error:', err);
        this.isLoading.set(false);
        this.toastService.show(this.translate('generator.toast.error'));
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
                alert(this.translate('generator.alert.saved'));
            },
            error: (err) => {
                console.error('Error:', err);
            }
        });
    }
}
