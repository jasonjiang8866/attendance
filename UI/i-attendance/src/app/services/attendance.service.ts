import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AttendanceRecord {
  name: string;
  timestamp: string;
  date: string;
}

export interface ApiResponse {
  success: boolean;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class AttendanceService {
  private baseUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  registerFace(name: string, imageFile: File): Observable<ApiResponse> {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('image', imageFile);
    
    return this.http.post<ApiResponse>(`${this.baseUrl}/register_face`, formData);
  }

  markAttendance(name: string): Observable<ApiResponse> {
    const formData = new FormData();
    formData.append('name', name);
    
    return this.http.post<ApiResponse>(`${this.baseUrl}/mark_attendance`, formData);
  }

  getAttendanceRecords(): Observable<{records: AttendanceRecord[]}> {
    return this.http.get<{records: AttendanceRecord[]}>(`${this.baseUrl}/attendance_records`);
  }

  getRegisteredFaces(): Observable<{faces: string[]}> {
    return this.http.get<{faces: string[]}>(`${this.baseUrl}/registered_faces`);
  }

  getVideoFeedUrl(): string {
    return `${this.baseUrl}/video_feed`;
  }
}
