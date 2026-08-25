import pandas as pd
 
dic_dim_track: list[dict] = [
    {
        "track_id": 101,
        "track_name": "Enter Sandman",
        "album_title": "Metallica",
        "artist_name": "Metallica",
        "genre_name": "Metal",
        "media_type_name": "MPEG audio file",
        "composer": "James Hetfield, Lars Ulrich, Kirk Hammett",
        "milliseconds": 331560,
        "bytes": 10874321,
    },
    {
        "track_id": 102,
        "track_name": "Master of Puppets",
        "album_title": "Master of Puppets",
        "artist_name": "Metallica",
        "genre_name": "Metal",
        "media_type_name": "MPEG audio file",
        "composer": "Hetfield, Ulrich, Burton, Hammett",
        "milliseconds": 515200,
        "bytes": 16843920,
    },
    {
        "track_id": 103,
        "track_name": "So What",
        "album_title": "Kind of Blue",
        "artist_name": "Miles Davis",
        "genre_name": "Jazz",
        "media_type_name": "AAC audio file",
        "composer": "Miles Davis",
        "milliseconds": 562000,
        "bytes": 18239014,
    },
]

dic_dim_customer: list[dict] = [
    {
        "customer_id": 1,
        "customer_full_name": "Luís Gonçalves",
        "company": "Embraer - Empresa Brasileira de Aeronáutica S.A.",
        "city": "São José dos Campos",
        "state": "SP",
        "country": "Brazil",
        "postal_code": "12227-000",
        "email": "luisg@embraer.com.br",
    },
    {
        "customer_id": 2,
        "customer_full_name": "Leonie Köhler",
        "company": None,
        "city": "Stuttgart",
        "state": "Baden-Württemberg",
        "country": "Germany",
        "postal_code": "70174",
        "email": "leonie.koehler@surfeu.de",
    },
    {
        "customer_id": 3,
        "customer_full_name": "François Tremblay",
        "company": None,
        "city": "Montréal",
        "state": "QC",
        "country": "Canada",
        "postal_code": "H2Y 1E6",
        "email": "ftremblay@gmail.com",
    },
]

dic_dim_employees: list[dict] = [
    {
        "employee_id": 1,
        "employee_full_name": "Andrew Adams",
        "title": "General Manager",
        "reports_to_name": None,
        "hire_date": "2020-08-14",
        "city": "Calgary",
        "country": "Canada",
    },
    {
        "employee_id": 2,
        "employee_full_name": "Nancy Edwards",
        "title": "Sales Manager",
        "reports_to_name": "Andrew Adams",
        "hire_date": "2021-05-01",
        "city": "Calgary",
        "country": "Canada",
    },
    {
        "employee_id": 3,
        "employee_full_name": "Jane Peacock",
        "title": "Sales Support Agent",
        "reports_to_name": "Nancy Edwards",
        "hire_date": "2022-04-01",
        "city": "Calgary",
        "country": "Canada",
    },
]

dic_dim_date: list[dict] = [
    {
        "date_key": 20260820,
        "full_date": "2026-08-20",
        "day_of_week": "Thursday",
        "month_number": 8,
        "month_name": "August",
        "quarter": "Q3",
        "year": 2026,
    },
    {
        "date_key": 20260821,
        "full_date": "2026-08-21",
        "day_of_week": "Friday",
        "month_number": 8,
        "month_name": "August",
        "quarter": "Q3",
        "year": 2026,
    },
]

dic_fact_sales: list[dict] = [
    {
        "fact_sales_id": 1,
        "invoice_id": 1001,
        "customer_id": 1,
        "track_id": 101,
        "invoice_date_key": 20260820,
        "unit_price": 0.99,
        "quantity": 1,
        "extended_amount": 0.99,
    },
    {
        "fact_sales_id": 2,
        "invoice_id": 1001,
        "customer_id": 1,
        "track_id": 102,
        "invoice_date_key": 20260820,
        "unit_price": 0.99,
        "quantity": 2,
        "extended_amount": 1.98,
    },
    {
        "fact_sales_id": 3,
        "invoice_id": 1002,
        "customer_id": 2,
        "track_id": 103,
        "invoice_date_key": 20260821,
        "unit_price": 1.29,
        "quantity": 1,
        "extended_amount": 1.29,
    },
]


dim_track = pd.DataFrame(dic_dim_track)
dim_customer = pd.DataFrame(dic_dim_customer)
dim_employees = pd.DataFrame(dic_dim_employees)
dim_sales = pd.DataFrame(dic_fact_sales)
dim_date = pd.DataFrame(dic_dim_date)
fact_sales = pd.DataFrame(dic_fact_sales)


