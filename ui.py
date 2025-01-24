from nicegui import ui
import asyncio

from patient_queue import PatientQueue
from models import Patient, Gender

queue = PatientQueue()
position = 0
ui.label("DoctorQ")
with ui.row():
    with ui.column():
        is_priority = ui.toggle({False: 'Zwykły', True: 'Priorytet'})
        with ui.column().bind_visibility_from(is_priority, 'value'):
            ui.number("Miejsce w kolejce pacjenta: ").bind_value(globals(), "position")
    with ui.column():
        name = ui.input("imię").classes('inline-flex').props('dense outlined')
        surname = ui.input("nazwisko").classes('inline-flex').props('dense outlined')
        pesel = ui.input("PESEL", validation = {"musi być 11 znaków": lambda e: len(e) == 11}).classes('inline-flex').props('dense outlined')
        age = ui.number("Wiek").classes('inline-flex').props('dense outlined')
        gender = ui.select({Gender.MALE.value: 'Mężczyzna', Gender.FEMALE.value: 'Kobieta', Gender.OTHER.value: 'Inne'}, label="Płeć", value=Gender.MALE.value).classes('inline-flex').props('dense outlined')
        appointment_time = ui.time().classes('inline-flex').props('dense outlined')
        async def sync():
            await asyncio.sleep(0)
            ui.notify("Dodano pacjenta")
            ui.notify(gender.value)
            patient = Patient(first_name=name.value, last_name=surname.value, pesel=pesel.value, age=age.value, gender=Gender[gender.value or ""], appointment_time=appointment_time.value)
            ui.notify(patient.model_dump_json())
            if is_priority:
                queue.add_priority_patient(patient, position)
            is_priority.set_value(any)
            name.set_value(any)
            surname.set_value(any)
            pesel.set_value(any)
            age.set_value(any)
            gender.set_value(any)
            appointment_time.set_value(any)
        ui.button("Zatwierdź", on_click=sync)
ui.run()