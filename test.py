from django.shortcuts import render
from time import timezone
from .models import Employee, Attendance
from django.shortcuts import render
import cv2
import numpy as np
from PIL import Image


def match_fingerprint(sample):


    best_score = counter = 0
    filename = image = kp1 = kp2 = mp = None
    for employee in Employee.objects.all():
        sift = cv2.SIFT_create()
        fingerprint_img = cv2.imread(employee.fingerprint.path)
        keypoints_1, des1 = sift.detectAndCompute(sample, None)
        keypoints_2, des2 = sift.detectAndCompute(fingerprint_img, None)
        # print(kp1, des1)
        # print(kp2, des2)
        # print(len(kp1), len(kp2))
        # print(len(des1), len(des2))
        # print(des1[0], des2[0])\
        # fast library for approx best match KNN
        matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(
            des1, des2, k=2
        )

        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = 0
        if len(keypoints_1) <= len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)
        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = employee.fingerprint
            image = fingerprint_img
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    print(f"Best match: {filename}")
    print("Best score:  " + str(best_score))


def clock_in(request):
    if request.method == 'POST':
        sample = cv2.imread(
            "/home/dasraev/PycharmProjects/fingerprint/media/fingerprints/100__M_Left_index_finger_CR.bmp")
        matched_fingerprint = match_fingerprint(sample)
        # employee = Employee.objects.get(fingerprint__exact=matched_fingerprint)
        # attendance = Attendance.objects.create(employee=employee, clock_in_time=timezone.now())
        # pass


    return render(request,'clockin.html')
def clock_out(request):
    # code to handle clocking out using fingerprint scanner
    # get sample fingerprint image from scanner
    sample = request.FILES.get('fingerprint')
    matched_fingerprint = match_fingerprint(sample)
    employee = Employee.objects.get(fingerprint__exact=matched_fingerprint)
    attendance = Attendance.objects.filter(employee=employee).latest('clock_in_time')
    attendance.clock_out_time = timezone.now()
    attendance.save()
    pass




def view_attendance(request):
    attendance_records = []
    for employee in Employee.objects.all():
        attendance_records.append({
            'employee': employee,
            'attendance': Attendance.objects.filter(employee=employee)
        })
    context = {'attendance_records': attendance_records}
    return render(request, 'attendance/view_attendance.html', context)
