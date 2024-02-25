from faker import Faker

fake = Faker()

form_data = {
    "first_name": fake.first_name(),
    "organization_name": fake.company(),
    "phone_number": fake.phone_number(),
    "email": fake.email(),
    "job_role": "Management",
}


