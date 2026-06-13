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
            'card.how_to_cook': 'How to cook',
            'generator.toast.refine.success': 'Recipe updated!',
            'generator.toast.refine.error': 'Error updating recipe',
            'generator.toast.save.success': 'Recipe saved!',
            'generator.toast.save.error': 'Error saving recipe',
            'catalog.toast.error': 'Error loading catalog',
            'favorites.toast.load.error': 'Error loading favorites',
            'favorites.toast.delete.success': 'Recipe removed from favorites',
            'favorites.toast.delete.error': 'Error removing recipe',
            'app.nav.settings': 'Settings',
            'settings.title': 'Profile & Goals',
            'settings.subtitle': 'Your data will be used to personalize AI-generated recipes',
            'settings.physical.title': 'Physical Parameters',
            'settings.height.label': 'Your height',
            'settings.height.placeholder': 'e.g. 175',
            'settings.height.unit': 'cm',
            'settings.height.hint': 'Affects calorie calculations in recipes',
            'settings.weight.label': 'Your weight',
            'settings.weight.placeholder': 'e.g. 70',
            'settings.weight.unit': 'kg',
            'settings.weight.hint': 'Used to calculate your daily nutritional needs',
            'settings.bmi': 'BMI',
            'settings.goal.title': 'Your Goal',
            'settings.goal.description': 'Select what you want to achieve. AI will adjust calorie content and macros in your recipes.',
            'settings.goal.lose': 'Weight Loss',
            'settings.goal.lose.desc': 'Calorie deficit, more protein',
            'settings.goal.maintain': 'Maintain Weight',
            'settings.goal.maintain.desc': 'Balanced and healthy nutrition',
            'settings.goal.gain': 'Muscle Gain',
            'settings.goal.gain.desc': 'Calorie surplus, high protein',
            'settings.ai.note': '🔮 Soon, AI will use your height, weight and goal to generate recipes with the perfect calorie count and macro split specifically for you.',
            'settings.save': 'Save Settings',
            'settings.saved': 'Saved!'
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
            'card.how_to_cook': 'Как готовить',
            'generator.toast.refine.success': 'Рецепт обновлен!',
            'generator.toast.refine.error': 'Ошибка обновления рецепта',
            'generator.toast.save.success': 'Рецепт сохранен!',
            'generator.toast.save.error': 'Ошибка сохранения рецепта',
            'catalog.toast.error': 'Ошибка загрузки каталога',
            'favorites.toast.load.error': 'Ошибка загрузки избранного',
            'favorites.toast.delete.success': 'Рецепт удален из избранного',
            'favorites.toast.delete.error': 'Ошибка удаления рецепта',
            'app.nav.settings': 'Настройки',
            'settings.title': 'Профиль и цели',
            'settings.subtitle': 'Ваши данные будут использоваться для персонализации рецептов от ИИ',
            'settings.physical.title': 'Физические параметры',
            'settings.height.label': 'Ваш рост',
            'settings.height.placeholder': 'например 175',
            'settings.height.unit': 'см',
            'settings.height.hint': 'Влияет на расчёт калорийности рецептов',
            'settings.weight.label': 'Ваш вес',
            'settings.weight.placeholder': 'например 70',
            'settings.weight.unit': 'кг',
            'settings.weight.hint': 'Используется для расчёта суточной нормы питания',
            'settings.bmi': 'ИМТ',
            'settings.goal.title': 'Ваша цель',
            'settings.goal.description': 'Выберите, чего вы хотите достичь. ИИ скорректирует калорийность и макросы в ваших рецептах.',
            'settings.goal.lose': 'Похудение',
            'settings.goal.lose.desc': 'Дефицит калорий, больше белка',
            'settings.goal.maintain': 'Поддержание веса',
            'settings.goal.maintain.desc': 'Сбалансированное и здоровое питание',
            'settings.goal.gain': 'Набор веса',
            'settings.goal.gain.desc': 'Профицит калорий, высокое содержание белка',
            'settings.ai.note': '🔮 Скоро ИИ будет использовать ваши рост, вес и цель для генерации рецептов с идеальной калорийностью и балансом макросов специально для вас.',
            'settings.save': 'Сохранить настройки',
            'settings.saved': 'Сохранено!'
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
