import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Recipe } from './models/all.i';

export interface Test {
    groupName: string;
    values: string;
}

@Injectable({
    providedIn: 'root'
})
export class RecipeService {
    private apiUrl = 'http://localhost:8000/api/recipes';

    constructor(private http: HttpClient) { }

    generateRecipe(query: string): Observable<Recipe> {
        return this.http.post<Recipe>(`${this.apiUrl}/generate`, { query });
    }

    refineRecipe(currentRecipe: Recipe, refinement: string): Observable<Recipe> {
        return this.http.post<Recipe>(`${this.apiUrl}/refine`, {
            current_recipe: currentRecipe,
            refinement: refinement
        });
    }
    saveRecipe(originalQuery: string, recipeData: Recipe): Observable<any> {
        return this.http.post(`${this.apiUrl}/save`, {
            original_query: originalQuery,
            recipe_data: recipeData
        });
    }

    getFavorites(): Observable<any> {
        return this.http.get(`${this.apiUrl}/favorites`);
    }

    getCatalog(): Observable<{catalog: Test[]}> {
        return this.http.get<{catalog: Test[]}>(`${this.apiUrl}/catalog`);
    }
}