import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RecipeService } from './api/api.service';
import { Recipe } from './api/models/all.i';

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  searchQuery: string = '';
  isLoading: boolean = false;

  currentRecipe: Recipe | null = null;
  originalQuery: string = '';

  refinementQuery: string = '';
  revisionsLeft: number = 2;

  isSaved: boolean = false;

  constructor(private recipeService: RecipeService, private cdr: ChangeDetectorRef) {
    this.currentRecipe = {
      "title": "Куриное филе с овощами на сковороде",
      "description": "Легкий и питательный ужин с куриным филе и свежими овощами, приготовленный на сковороде. Отличный вариант для тех, кто следит за фигурой и ценит быстроту приготовления.",
      "macros": {
        "calories": 310,
        "protein_g": 37,
        "fat_g": 9,
        "carbs_g": 20
      },
      "prep_time_minutes": 30,
      "ingredients": [
        {
          "name": "Куриное филе",
          "amount": "150г"
        },
        {
          "name": "Брокколи",
          "amount": "150г"
        },
        {
          "name": "Перец болгарский",
          "amount": "100г"
        },
        {
          "name": "Цукини",
          "amount": "100г"
        },
        {
          "name": "Оливковое масло",
          "amount": "1 ч.л."
        },
        {
          "name": "Соль",
          "amount": "по вкусу"
        },
        {
          "name": "Черный перец",
          "amount": "по вкусу"
        },
        {
          "name": "Сушеный чеснок",
          "amount": "по вкусу"
        }
      ],
      "steps": [
        "Куриное филе промойте, обсушите и нарежьте небольшими кусочками или полосками. Посолите, поперчите и посыпьте сушеным чесноком.",
        "Брокколи разделите на соцветия. Болгарский перец очистите от семян и нарежьте соломкой. Цукини нарежьте полукольцами или кубиками.",
        "Разогрейте сковороду с оливковым маслом на среднем огне. Выложите куриное филе и обжаривайте 5-7 минут до золотистой корочки, периодически помешивая.",
        "Добавьте на сковороду брокколи, болгарский перец и цукини. Перемешайте. Обжаривайте овощи вместе с курицей еще 10-12 минут, пока овощи не станут мягкими, но сохранят легкую хрусткость.",
        "Подавайте блюдо горячим."
      ],
      "substitutions": [
        "Куриное филе можно заменить на филе индейки.",
        "Брокколи можно заменить на цветную капусту или стручковую фасоль.",
        "Цукини можно заменить на баклажан или грибы.",
        "Оливковое масло можно заменить на кокосовое масло или использовать антипригарный спрей для минимизации жира."
      ]
    };
  }

  generateRecipe() {
    if (!this.searchQuery.trim()) return;

    this.isLoading = true;
    this.currentRecipe = null;
    this.isSaved = false;
    this.revisionsLeft = 2;
    this.originalQuery = this.searchQuery;

    this.recipeService.generateRecipe(this.searchQuery).subscribe({
      next: (recipe) => {
        console.log('currentRecipe', recipe);
        this.currentRecipe = recipe;
        this.isLoading = false;
        console.log('currentRecipe', this.currentRecipe);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка генерации:', err);
        this.isLoading = false;
        alert('Произошла ошибка при обращении к API.');
      }
    });
  }

  refineRecipe() {
    if (!this.refinementQuery.trim() || !this.currentRecipe || this.revisionsLeft <= 0) return;

    this.isLoading = true;
    this.recipeService.refineRecipe(this.currentRecipe, this.refinementQuery).subscribe({
      next: (updatedRecipe) => {
        this.currentRecipe = updatedRecipe;
        this.revisionsLeft--;
        this.refinementQuery = '';
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Ошибка обновления:', err);
        this.isLoading = false;
      }
    });
  }

  saveRecipe() {
    if (!this.currentRecipe) return;

    this.recipeService.saveRecipe(this.originalQuery, this.currentRecipe).subscribe({
      next: () => {
        this.isSaved = true;
        alert('Рецепт успешно сохранен в Избранное!');
      },
      error: (err) => {
        console.error('Ошибка сохранения:', err);
      }
    });
  }
}
