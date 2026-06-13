import { Component, inject, signal } from '@angular/core';
import { ToastService, ToastType } from '../../services/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [],
  template: `
    @if (message()) {
      <div [class]="'toast ' + type()" [style.--duration.ms]="duration">
        <div class="toast-icon">
          @if (type() === 'success') {
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M20 6L9 17L4 12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          } @else if (type() === 'error') {
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          } @else {
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4M12 8h.01" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          }
        </div>
        <div class="toast-message">{{ message() }}</div>
      </div>
    }
  `,
  styleUrls: ['./toast.component.css']
})
export class ToastComponent {
  private toastService = inject(ToastService);
  message = signal<string | null>(null);
  type = signal<ToastType>('info');
  duration = 3000;

  constructor() {
    this.toastService.getToast$().subscribe(toast => {
      this.message.set(toast.msg);
      this.type.set(toast.type ?? 'info');
      this.duration = toast.duration ?? 3000;
      setTimeout(() => this.message.set(null), this.duration);
    });
  }
}
