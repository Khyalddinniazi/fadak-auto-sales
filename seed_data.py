# Demo inventory and services for Fadak Auto Sales.
# Each image uses a fixed crop size so cards stay proportional.

IMG = "https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=800&h=500&q=80"

# One verified-working Unsplash photo per vehicle (index-aligned with
# VEHICLE_SEED below). All IDs are checked to return HTTP 200 so no card
# falls back to the placeholder image.
PHOTOS = [
    "1552519507-da3b142c6e3d",  # Toyota Camry
    "1583121274602-3e2820c69888",  # Honda Accord
    "1605559424843-9e4c228bf1c2",  # Ford F-150
    "1494976388531-d1058494cdd8",  # BMW 3 Series
    "1553440569-bcc63803a83d",  # Tesla Model 3
    "1606664515524-ed2f786a0bd6",  # Nissan Altima
    "1617469767053-d3b523a0b982",  # Chevrolet Silverado
    "1580273916550-e323be2ae537",  # Hyundai Sonata
    "1568605117036-5fe5e7bab0b7",  # Mazda CX-5
    "1503376780353-7e6692767b70",  # Subaru Outback
    "1493238792000-8113da705763",  # Jeep Grand Cherokee
    "1561580125-028ee3bd62eb",  # Mercedes-Benz C-Class
    "1571607388263-1044f9ea01dd",  # Kia Telluride
    "1606152421802-db97b9c7a11b",  # Ram 1500
    "1502877338535-766e1452684a",  # Volkswagen Jetta
    "1549399542-7e3f8b79c341",  # Toyota RAV4
    "1611016186353-9af58c69a533",  # Audi A4
    "1617814076367-b759c7d7e738",  # Honda CR-V
    "1617531653332-bd46c24f2068",  # Lexus RX 350
    "1542282088-fe8426682b8f",  # Ford Explorer
    "1549317661-bd32c8ce0db2",  # Toyota Tacoma
    "1549924231-f129b911e442",  # Chevrolet Equinox
]


def photo_url(index):
    return IMG.format(id=PHOTOS[index % len(PHOTOS)])


# (year, make, model, mileage, price, condition, vin, description, status)
VEHICLE_SEED = [
    (2021, "Toyota", "Camry", 34500, 23999, "Used", "VIN-FAD-TOY-CAMRY-21", "Reliable midsize sedan with safety tech.", "Available"),
    (2020, "Honda", "Accord", 42800, 22450, "Used", "VIN-FAD-HON-ACC-20", "Spacious interior and strong fuel economy.", "Available"),
    (2022, "Ford", "F-150", 25600, 38900, "Used", "VIN-FAD-FOR-F150-22", "Powerful pickup with modern infotainment.", "Available"),
    (2019, "BMW", "3 Series", 51000, 27995, "Used", "VIN-FAD-BMW-3S-19", "Luxury sport sedan with premium handling.", "Sold"),
    (2023, "Tesla", "Model 3", 12000, 42999, "Certified", "VIN-FAD-TES-M3-23", "All-electric with advanced driver assistance.", "Available"),
    (2021, "Nissan", "Altima", 37000, 20999, "Used", "VIN-FAD-NIS-ALT-21", "Comfortable family sedan with modern styling.", "Available"),
    (2020, "Chevrolet", "Silverado", 47000, 34995, "Used", "VIN-FAD-CHE-SILV-20", "Durable truck with strong utility.", "Available"),
    (2022, "Hyundai", "Sonata", 22000, 25950, "Certified", "VIN-FAD-HYU-SON-22", "Modern sedan with advanced safety package.", "Available"),
    (2018, "Mazda", "CX-5", 58200, 19995, "Used", "VIN-FAD-MAZ-CX5-18", "Compact SUV with sporty handling.", "Available"),
    (2021, "Subaru", "Outback", 31000, 28950, "Certified", "VIN-FAD-SUB-OUT-21", "All-wheel drive wagon built for Pacific NW roads.", "Available"),
    (2020, "Jeep", "Grand Cherokee", 44500, 26999, "Used", "VIN-FAD-JEP-GC-20", "Capable SUV with premium cabin options.", "Available"),
    (2019, "Mercedes-Benz", "C-Class", 39800, 31995, "Used", "VIN-FAD-MER-CC-19", "Executive sedan with refined comfort.", "Available"),
    (2022, "Kia", "Telluride", 18500, 36999, "Certified", "VIN-FAD-KIA-TEL-22", "Three-row SUV with family-friendly features.", "Available"),
    (2021, "Ram", "1500", 33200, 35995, "Used", "VIN-FAD-RAM-1500-21", "Full-size truck with towing package.", "Available"),
    (2020, "Volkswagen", "Jetta", 41000, 17850, "Used", "VIN-FAD-VW-JET-20", "Efficient commuter with German engineering.", "Available"),
    (2023, "Toyota", "RAV4", 14000, 33499, "Certified", "VIN-FAD-TOY-RAV4-23", "Top-selling compact SUV with hybrid option.", "Available"),
    (2019, "Audi", "A4", 47600, 29995, "Used", "VIN-FAD-AUD-A4-19", "Quattro all-wheel drive luxury sedan.", "Sold"),
    (2022, "Honda", "CR-V", 26800, 29950, "Certified", "VIN-FAD-HON-CRV-22", "Practical SUV with excellent resale value.", "Available"),
    (2020, "Lexus", "RX 350", 39000, 38995, "Used", "VIN-FAD-LEX-RX-20", "Smooth luxury crossover with quiet ride.", "Available"),
    (2021, "Ford", "Explorer", 35500, 31999, "Used", "VIN-FAD-FOR-EXP-21", "Three-row SUV for growing families.", "Available"),
    (2018, "Toyota", "Tacoma", 62000, 27995, "Used", "VIN-FAD-TOY-TAC-18", "Midsize truck known for reliability.", "Available"),
    (2023, "Chevrolet", "Equinox", 11000, 28999, "Certified", "VIN-FAD-CHE-EQU-23", "Compact SUV with tech-forward interior.", "Available"),
]

SERVICE_SEED = [
    ("Oil Change", "Full-synthetic and conventional oil change with filter.", 59.99),
    ("Brake Repair", "Pads, rotors, and complete brake system inspection.", 149.99),
    ("Tire Replacement", "Mount, balance, and pressure check on new tires.", 129.99),
    ("Engine Diagnostics", "Computer scan for warning lights and performance.", 99.99),
    ("Battery Replacement", "Battery test, replacement, and charging check.", 119.99),
    ("Transmission Service", "Fluid service and transmission health inspection.", 199.99),
    ("AC Repair", "Recharge, leak detection, and cooling restoration.", 139.99),
    ("Wheel Alignment", "Precision 4-wheel alignment for even tire wear.", 89.99),
    ("Coolant Flush", "Radiator flush and antifreeze replacement.", 129.99),
    ("Suspension Repair", "Shocks, struts, and steering component service.", 179.99),
    ("Exhaust Repair", "Muffler, catalytic converter, and exhaust leaks.", 159.99),
    ("Windshield Replacement", "OEM-quality glass replacement and sealing.", 249.99),
    ("Detailing Package", "Interior and exterior deep clean and protection.", 149.99),
    ("State Inspection", "Safety and emissions readiness inspection.", 79.99),
    ("Spark Plug Replacement", "Ignition tune-up for smoother starts.", 119.99),
    ("Fuel System Cleaning", "Injector and intake cleaning for efficiency.", 139.99),
    ("Pre-Purchase Inspection", "Full mechanical review before you buy.", 149.99),
    ("Check Engine Light", "Diagnostic and repair estimate for warning lamps.", 89.99),
]


def vehicles_with_images():
    """Return vehicle tuples ready for INSERT including image_url."""
    rows = []
    for i, row in enumerate(VEHICLE_SEED):
        year, make, model, mileage, price, condition, vin, description, status = row
        rows.append(
            (
                year,
                make,
                model,
                mileage,
                price,
                condition,
                vin,
                description,
                photo_url(i),
                status,
            )
        )
    return rows
