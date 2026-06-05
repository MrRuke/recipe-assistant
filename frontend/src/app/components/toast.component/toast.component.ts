import { CommonModule, NgIf } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [CommonModule, NgIf],
  template: `
    <div *ngIf="message()" class="toast" [style.--duration.ms]="duration">
      {{ message() }}
    </div>
  `,
  styleUrls: ['./toast.component.css']
})
export class ToastComponent {
  private toastService = inject(ToastService);
  message = signal<string | null>(null);
  duration = 3000;

  constructor() {
    this.toastService.getToast$().subscribe(toast => {
      this.message.set(toast.msg);
      this.duration = toast.duration ?? 33000;
      setTimeout(() => this.message.set(null), this.duration);
    });
  }
}
