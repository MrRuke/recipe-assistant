export interface Macros {
    calories: number;
    protein_g: number;
    fat_g: number;
    carbs_g: number;
}

export interface Ingredient {
    name: string;
    amount: string;
}

export interface Recipe {
    title: string;
    description: string;
    macros: Macros;
    prep_time_minutes: number;
    ingredients: Ingredient[];
    steps: string[];
    substitutions: string[];
}

export interface SavedRecipe {
    id: number;
    title: string;
    recipe_data: Recipe; // Внутри лежит наш обычный рецепт
    created_at: string;
}