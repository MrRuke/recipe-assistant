import { Routes } from '@angular/router';
import { GeneratorComponent } from './pages/generator/generator.component';
import { FavoritesComponent } from './pages/favorites/favorites.component';

export const routes: Routes = [
    { path: '', component: GeneratorComponent },
    { path: 'favorites', component: FavoritesComponent },
    { path: '**', redirectTo: '' }
];