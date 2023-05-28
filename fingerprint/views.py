from django.utils import timezone
from .models import Student, Attendance
from django.shortcuts import render
import cv2
import numpy as np
from PIL import Image
from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max

def login_view(request):
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('attendance')
        else:
            messages.error(request,"Username or password is wrong")
    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('clockin')

def match_fingerprint(sample):

    best_score = counter = 0
    filename = image = kp1 = kp2 = mp = None
    for student in Student.objects.all():
        sift = cv2.SIFT_create()
        fingerprint_img = cv2.imread(student.fingerprint.path)
        keypoints_1, des1 = sift.detectAndCompute(sample, None)
        keypoints_2, des2 = sift.detectAndCompute(fingerprint_img, None)

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
            filename = student.fingerprint
            image = fingerprint_img
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points
    if best_score >= 50:
        return filename

def clock_in(request):
    if request.method == 'POST':
        sample = request.FILES['fingerprint']
        sample = np.array(Image.open(sample))
        matched_fingerprint = match_fingerprint(sample)
        try:
            student = Student.objects.get(fingerprint__exact=matched_fingerprint)
            attendance = Attendance.objects.create(student=student, clock_in_time=timezone.now())
            messages.success(request,'BARMOQ IZI MOS KELDI')

            return redirect('clockin')
        except Student.DoesNotExist:
            messages.error(request,'BARMOQ IZI MOS KELMADI, ILTIMOS QAYTADAN URINIB KO\'RING')
            return redirect('clockin')
    return render(request,'clockin.html')


def clock_out(request):
    if request.method == 'POST':
        sample = request.FILES.get('fingerprint')
        sample = np.array(Image.open(sample))
        matched_fingerprint = match_fingerprint(sample)
        try:
            student = Student.objects.get(fingerprint__exact=matched_fingerprint)
            messages.success(request,'BARMOQ IZI MOS KELDI')
        except Student.DoesNotExist:
            messages.error(request,'BARMOQ IZI MOS KELMADI, ILTIMOS QAYTADAN URINIB KO\'RING')
            return redirect('clockout')
        try:
            attendance = Attendance.objects.filter(student=student).latest('clock_in_time')
            attendance.clock_out_time = timezone.now()
            attendance.save()
        except Attendance.DoesNotExist:
            pass
        return redirect('clockout')

    return render(request,'clockout.html')


@login_required
def view_attendance(request):
    page_num = request.GET.get('page', 1)
    today = datetime.today()
    attendance_records = []
    for student in Student.objects.annotate(
    last_clock_in=Max('attendances__clock_in_time')
).order_by('-last_clock_in'):
        attendance_records.append({
            'student': student,
            'attendance': Attendance.objects.filter(Q(student=student) & (Q(clock_in_time__date=today) | Q(clock_out_time__date=today)) ).last()
        })
    context = {'attendance_records': attendance_records}
    paginator = Paginator(attendance_records, 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    print(context['attendance_records'])
    return render(request, 'view_attendance.html', {'page_obj':page_obj})

def student_attendances(request,pk):
    page_num = request.GET.get('page', 1)

    student = get_object_or_404(Student,pk=pk)
    attendances = Attendance.objects.filter(student=student)
    paginator = Paginator(attendances, 5)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'student_attendances.html',{'page_obj':page_obj})


