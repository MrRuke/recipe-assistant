import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

export type ToastType = 'success' | 'error' | 'info';

export interface ToastMessage {
  msg: string;
  type?: ToastType;
  duration?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private toastSubject = new Subject<ToastMessage>();

  show(message: string, type: ToastType = 'info', duration: number = 3000): void {
    this.toastSubject.next({ msg: message, type, duration });
  }

  getToast$(): Observable<ToastMessage> {
    return this.toastSubject.asObservable();
  }
}
