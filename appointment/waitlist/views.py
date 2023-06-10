from django.shortcuts import render, redirect
from .models import Doctor, Patient
from datetime import timedelta
import random
from django.utils import timezone

# Create your views here.
data = [
    {
        "firstname": "Toto",
        "lastname": "Wolff",
        "specialty": "General Practitioner"
    },
    {
        "firstname": "Eden",
        "lastname": "Hazard",
        "specialty": "General Practitioner"
    },
    {
        "firstname": "Lewis",
        "lastname": "Hamilton",
        "specialty": "General Practitioner"
    }
]


def add_data(data):
    "Adds doctors to the database"
    for doc in data:
        firstname = doc["firstname"]
        lastname = doc["lastname"]
        specialty = doc["specialty"]

        Doctor.objects.get_or_create(firstname=firstname,
                                     lastname=lastname,
                                     specialty=specialty)


# Uncomment the line below after performing database migration
add_data(data)


def time_plus(date_obj, timedelta):
    end = date_obj + timedelta
    return end


taken = []


def pick_doctor(doctors):
    """Chooses a doctor that is not yet taken"""
    if len(taken) == len(doctors):
        # print(taken)
        taken.clear()
    one = None
    while True:
        one = random.choice(doctors)
        if one not in taken:
            taken.append(one)
            return one


def home(request):
    # Get all doctors
    doctors = list(Doctor.objects.all())

    my_message = False
    if request.method == "POST":
        print(request.POST)
        patient_info = [v[0] for _, v in dict(request.POST).items()]
        print(patient_info)
        firstname = patient_info[1]
        lastname = patient_info[2]
        patient_no = int(patient_info[4])

        doctor = pick_doctor(doctors)

        # print(taken)
        patients = list(Patient.objects.all())
        # Get current time
        now = timezone.localtime(timezone.now())

        if patients:
            try:
                doc_patients = list(Patient.objects.filter(
                    doctor=doctor))
                latest = doc_patients[-1]

                f_app_time = latest.appoint_time

                next_app_time = time_plus(f_app_time, timedelta(minutes=25))

                if now > next_app_time:
                    next_app_time = time_plus(
                        now, timedelta(minutes=25))

                appoint_time = next_app_time

                new_patient = Patient(firstname=firstname,
                                      lastname=lastname,
                                      doctor=doctor,
                                      appoint_time=appoint_time,
                                      patient_no=patient_no)
                new_patient.save()
                my_message = f"Hey {firstname} {lastname}, the time of your appointment is {appoint_time.strftime('%I:%M %p')}"
                request.session['msg'] = my_message
                return redirect(request.path)
            except:
                appoint_time = time_plus(now, timedelta(minutes=25))

                # First Patient for this doctor
                first_patient = Patient(firstname=firstname,
                                        lastname=lastname,
                                        doctor=doctor,
                                        appoint_time=appoint_time,
                                        patient_no=patient_no)
                first_patient.save()
                my_message = f"Hey {firstname} {lastname}, the time of your appointment is {appoint_time.strftime('%I:%M %p')}"
                request.session['msg'] = my_message
                return redirect(request.path)
        else:
            appoint_time = time_plus(now, timedelta(minutes=25))

            first_patient = Patient(firstname=firstname,
                                    lastname=lastname,
                                    doctor=doctor,
                                    appoint_time=appoint_time,
                                    patient_no=patient_no)
            first_patient.save()
            my_message = f"Hello {firstname} {lastname}, your estimated appointment time is {appoint_time.strftime('%I:%M %p')} We appreciate your patience and look forward to providing you with exceptional care."
            # my_message = f"Hey {firstname} {lastname}, the time of your appointment is {appoint_time.strftime('%I:%M %p')}"
            request.session['msg'] = my_message
            return redirect(request.path)

    msg = request.session.get('msg', False)
    if msg:
        del request.session['msg']
    return render(request, 'waitlist/home.html', {'doctors': doctors,
                                                  'msg': msg})


def table(request):
    """View for Waitlist table"""
    patients = Patient.objects.all()
    return render(request, 'waitlist/table.html', {'patients': patients})


def contact(request):
    """View for Waitlist contact"""
    patients = Patient.objects.all()
    my_message = False
    if request.method == "POST":
        my_message = "Message sent, thank you!"
        request.session['msg'] = my_message
        return redirect(request.path)

    msg = request.session.get('msg', False)
    if msg:
        del request.session['msg']
    return render(request, 'waitlist/contact.html', {'patients': patients,
                                                     'msg': msg})

def doctors(request):
    """View for Waitlist contact"""
    patients = Patient.objects.all()
    return render(request, 'waitlist/doctors.html', {'patients': patients})