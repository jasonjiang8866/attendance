import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AttendanceService, AttendanceRecord } from '../services/attendance.service';

@Component({
  selector: 'app-attendance',
  templateUrl: './attendance.component.html',
  styleUrls: ['./attendance.component.css']
})
export class AttendanceComponent implements OnInit {
  registrationForm: FormGroup;
  attendanceForm: FormGroup;
  attendanceRecords: AttendanceRecord[] = [];
  registeredFaces: string[] = [];
  selectedFile: File | null = null;
  videoFeedUrl: string;
  selectedTabIndex = 0;
  
  // Loading states
  isLoading = false;
  isMarkingAttendance = false;
  isLoadingRecords = false;
  videoError = false;

  constructor(
    private fb: FormBuilder,
    private attendanceService: AttendanceService,
    private snackBar: MatSnackBar
  ) {
    this.registrationForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]]
    });

    this.attendanceForm = this.fb.group({
      name: ['', Validators.required]
    });

    this.videoFeedUrl = this.attendanceService.getVideoFeedUrl();
  }

  ngOnInit() {
    this.loadRegisteredFaces();
    this.loadAttendanceRecords();
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      this.selectedFile = file;
    } else {
      this.showMessage('Please select a valid image file');
    }
  }

  onRegisterFace() {
    if (this.registrationForm.valid && this.selectedFile) {
      const name = this.registrationForm.get('name')?.value;
      this.isLoading = true;
      
      this.attendanceService.registerFace(name, this.selectedFile).subscribe({
        next: (response) => {
          this.isLoading = false;
          if (response.success) {
            this.showMessage(`✅ ${response.message}`);
            this.registrationForm.reset();
            this.selectedFile = null;
            this.loadRegisteredFaces();
          } else {
            this.showMessage(`❌ Registration failed: ${response.message}`);
          }
        },
        error: (error) => {
          this.isLoading = false;
          this.showMessage(`❌ Registration failed: ${error.message || 'Connection error'}`);
        }
      });
    } else {
      this.showMessage('Please fill in your name and select an image file');
    }
  }

  onMarkAttendance() {
    if (this.attendanceForm.valid) {
      const name = this.attendanceForm.get('name')?.value;
      this.isMarkingAttendance = true;
      
      this.attendanceService.markAttendance(name).subscribe({
        next: (response) => {
          this.isMarkingAttendance = false;
          if (response.success) {
            this.showMessage(`✅ ${response.message}`);
            this.attendanceForm.reset();
            this.loadAttendanceRecords();
          } else {
            this.showMessage(`⚠️ ${response.message}`);
          }
        },
        error: (error) => {
          this.isMarkingAttendance = false;
          this.showMessage(`❌ Failed to mark attendance: ${error.message || 'Connection error'}`);
        }
      });
    }
  }

  loadRegisteredFaces() {
    this.attendanceService.getRegisteredFaces().subscribe({
      next: (response) => {
        this.registeredFaces = response.faces;
      },
      error: (error) => {
        console.error('Failed to load registered faces:', error);
      }
    });
  }

  loadAttendanceRecords() {
    this.isLoadingRecords = true;
    this.attendanceService.getAttendanceRecords().subscribe({
      next: (response) => {
        this.isLoadingRecords = false;
        this.attendanceRecords = response.records.sort((a, b) => 
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        );
      },
      error: (error) => {
        this.isLoadingRecords = false;
        console.error('Failed to load attendance records:', error);
        this.showMessage('❌ Failed to load attendance records. Please check your connection.');
      }
    });
  }

  formatDateTime(timestamp: string): string {
    return new Date(timestamp).toLocaleString();
  }

  formatDate(date: string): string {
    return new Date(date).toLocaleDateString();
  }

  onVideoError(event: any) {
    const target = event.target as HTMLImageElement;
    this.videoError = true;
    console.warn('Video feed error:', event);
  }

  retryVideoFeed() {
    this.videoError = false;
    // Force reload the video feed by adding a timestamp
    this.videoFeedUrl = `${this.attendanceService.getVideoFeedUrl()}?t=${Date.now()}`;
  }

  private showMessage(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top'
    });
  }
}
