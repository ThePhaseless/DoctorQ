import datetime

from nicegui import ui

from models import Gender, Patient
from patient_queue import PatientQueue

queue = PatientQueue()

ui.label("DoctorQ")
with ui.row():
    is_priority: ui.toggle
    position: ui.number
    name: ui.input
    with ui.column():
        is_priority = ui.toggle(
            {False: "Zwykły", True: "Priorytet"},
            on_change=lambda e: ui.notify(e),
            value=False,
        )
        with ui.column().bind_visibility_from(is_priority, "value"):
            position = ui.number(
                "Miejsce w kolejce: ",
            )
    with ui.column():
        name = ui.input("imię").classes("inline-flex").props("dense outlined")
        surname = ui.input("nazwisko").classes("inline-flex").props("dense outlined")
        pesel = (
            ui.input(
                "PESEL",
                validation={"musi być 11 znaków": lambda e: not e or len(e) == 11},
            )
            .classes("inline-flex")
            .props("dense outlined")
        )
        age = ui.number("Wiek").classes("inline-flex").props("dense outlined")
        gender = (
            ui.select(
                {
                    Gender.MALE.value: "Mężczyzna",
                    Gender.FEMALE.value: "Kobieta",
                    Gender.OTHER.value: "Inne",
                },
                label="Płeć",
                value=Gender.MALE.value,
            )
            .classes("inline-flex")
            .props("dense outlined")
        )
        appointment_time = ui.time().classes("inline-flex").props("dense outlined")

        def add_patient():
            patient = Patient(
                first_name=name.value,
                last_name=surname.value,
                pesel=pesel.value,
                age=age.value,
                gender=Gender[gender.value or ""],
                appointment_time=datetime.datetime.today()
                + datetime.timedelta(
                    hours=int(appointment_time.value.split(":")[0] or 0),
                    minutes=int(appointment_time.value.split(":")[1] or 0),
                ),
            )
            ui.notify(f"Dodano pacjenta: {patient.first_name} {patient.last_name}")
            if is_priority and position:
                queue.add_priority_patient(patient, position.value)
                is_priority.set_value(None)
            name.set_value(None)
            surname.set_value(None)
            pesel.set_value(None)
            age.set_value(None)
            gender.set_value(None)
            appointment_time.set_value(None)

        ui.button("Zatwierdź", on_click=add_patient)
ui.run()
