import { Routes } from '@angular/router';
import { CatalogComponent } from './pages/catalog/catalog.component';
import { FavoritesComponent } from './pages/favorites/favorites.component';
import { GeneratorComponent } from './pages/generator/generator.component';
import { SettingsComponent } from './pages/settings/settings.component';

export const routes: Routes = [
    { path: '', component: GeneratorComponent },
    { path: 'favorites', component: FavoritesComponent },
    { path: 'catalog', component: CatalogComponent },
    { path: 'settings', component: SettingsComponent },
    { path: '**', redirectTo: '' }
];