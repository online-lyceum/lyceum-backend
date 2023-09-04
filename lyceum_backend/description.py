with open('./lyceum_backend/description.md', encoding='utf-8') as file:
    description = file.read()

application_metadata = {
    "title": "API для TimeManager",
    "description": description,
    "version": "0.0.1.dev1",
}
