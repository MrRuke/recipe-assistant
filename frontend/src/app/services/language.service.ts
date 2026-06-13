import { Injectable, signal } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class LanguageService {
    public language = signal<'en' | 'ru'>('en');

    private translations: Record<'en' | 'ru', Record<string, string>> = {
        en: {
            'app.title': 'AI Recipe Assistant',
            'app.nav.create': 'Create recipe',
            'app.nav.favorites': 'My favorites',
            'app.nav.catalog': 'Catalog',
            'generator.input.placeholder': 'What recipe do you need? (for example: a chicken dinner under 400 kcal)',
            'generator.btn.create': 'Create recipe',
            'generator.btn.generating': 'Generating...',
            'generator.toast.generating': 'Generating recipe...',
            'generator.toast.success': 'Recipe generated!',
            'generator.toast.error': 'Error generating recipe',
            'generator.edits.remaining': 'Edits remaining: ',
            'generator.input.refine.placeholder': 'What would you change? (For example: replace chicken with turkey)',
            'generator.btn.refine': 'Update recipe',
            'generator.btn.save': 'Save',
            'generator.btn.saved': 'Saved',
            'generator.alert.saved': 'Saved!',
            'generator.loading': 'Generating recipe...',
            'favorites.title': 'Saved recipes',
            'favorites.empty': 'You do not have saved recipes',
            'favorites.btn.back': 'Go back',
            'favorites.btn.open': 'Open details',
            'favorites.confirm.title': 'Remove from favorites?',
            'favorites.confirm.text': 'Are you sure you want to remove ',
            'favorites.confirm.text2': ' from your favorites?',
            'favorites.btn.cancel': 'Cancel',
            'favorites.btn.delete': 'Delete',
            'catalog.title': 'Recipes from database:',
            'card.prep_time': 'min',
            'card.calories': 'kcal',
            'card.protein': 'Protein',
            'card.fat': 'Fat',
            'card.carbs': 'Carbs',
            'card.ingredients': 'Ingredients',
            'card.substitutions': 'Substitutions',
            'card.how_to_cook': 'How to cook'
        },
        ru: {
            'app.title': 'AI Recipe Assistant',
            'app.nav.create': 'Создать рецепт',
            'app.nav.favorites': 'Мое избранное',
            'app.nav.catalog': 'Каталог',
            'generator.input.placeholder': 'Какой рецепт вам нужен? (например: ужин с курицей до 400 ккал)',
            'generator.btn.create': 'Создать рецепт',
            'generator.btn.generating': 'Генерация...',
            'generator.toast.generating': 'Создание рецепта...',
            'generator.toast.success': 'Рецепт создан!',
            'generator.toast.error': 'Ошибка генерации рецепта',
            'generator.edits.remaining': 'Осталось изменений: ',
            'generator.input.refine.placeholder': 'Что бы вы изменили? (Например: заменить курицу на индейку)',
            'generator.btn.refine': 'Обновить рецепт',
            'generator.btn.save': 'Сохранить',
            'generator.btn.saved': 'Сохранено',
            'generator.alert.saved': 'Сохранено!',
            'generator.loading': 'Создание рецепта...',
            'favorites.title': 'Сохраненные рецепты',
            'favorites.empty': 'У вас нет сохраненных рецептов',
            'favorites.btn.back': 'Назад',
            'favorites.btn.open': 'Открыть детали',
            'favorites.confirm.title': 'Удалить из избранного?',
            'favorites.confirm.text': 'Вы уверены, что хотите удалить ',
            'favorites.confirm.text2': ' из избранного?',
            'favorites.btn.cancel': 'Отмена',
            'favorites.btn.delete': 'Удалить',
            'catalog.title': 'Рецепты из базы данных:',
            'card.prep_time': 'мин',
            'card.calories': 'ккал',
            'card.protein': 'Белки',
            'card.fat': 'Жиры',
            'card.carbs': 'Углеводы',
            'card.ingredients': 'Ингредиенты',
            'card.substitutions': 'Замены',
            'card.how_to_cook': 'Как готовить'
        }
    };

    constructor() {
        const savedLang = localStorage.getItem('language');
        if (savedLang === 'ru' || savedLang === 'en') {
            this.language.set(savedLang);
        }
    }

    setLanguage(lang: 'en' | 'ru') {
        this.language.set(lang);
        localStorage.setItem('language', lang);
    }

    translate(key: string): string {
        const currentLang = this.language();
        return this.translations[currentLang][key] || key;
    }
}
