import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

interface ToastMessage {
  msg: string;
  duration?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private toastSubject = new Subject<ToastMessage>();

  show(message: string, duration: number = 3000): void {
    this.toastSubject.next({ msg: message, duration });
  }

  getToast$(): Observable<ToastMessage> {
    return this.toastSubject.asObservable();
  }
}
