import os

from sqlmodel import Session, SQLModel, create_engine, select

from backend.models import Dish

# --- Database Setup ---
DATABASE_URL = "sqlite:///singapore_food.db"
DATABASE_FILE = "singapore_food.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Creates the database and tables if they don't exist."""
    print("=" * 50)
    print("Singapore Makan Recommender Starting Up")
    print("=" * 50)

    db_exists = os.path.exists(DATABASE_FILE)

    if db_exists:
        print(f"Database '{DATABASE_FILE}' already exists. Using existing database.")
    else:
        print(f"Database '{DATABASE_FILE}' not found. Creating new database.")

    # Create tables if they don't exist (this is safe even if DB exists)
    SQLModel.metadata.create_all(engine)

    print("Server will be available at:")
    print("   - Web Interface: http://127.0.0.1:8000/")
    print("   - API Documentation: http://127.0.0.1:8000/docs")
    print("   - API Endpoints: http://127.0.0.1:8000/dishes, http://127.0.0.1:8000/recommend")
    print("=" * 50)


def seed_database():
    """Populates the database with a hyper-realistic list of Singaporean dishes."""
    with Session(engine) as session:
        existing_dish = session.exec(select(Dish)).first()
        if existing_dish:
            print("Database already contains dishes. Skipping seed operation.")
            print("Ready to serve recommendations!")
            print("=" * 50)
            return

        print("Database is empty. Seeding with Singapore dishes...")
        dishes = [
            # === RICE-BASED MAINS ===
            Dish(
                name="Hainanese Chicken Rice",
                description="Poached chicken with fragrant oily rice and chilli sauce.",
                price=5.50,
                cuisine="Chinese",
                spiciness=1,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Rice", "Popular", "Comfort"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Nasi Lemak",
                description=(
                    "Coconut rice with sambal chili, fried chicken wing, egg, and "
                    "ikan bilis."
                ),
                price=6.50,
                cuisine="Malay",
                spiciness=7,
                meal_time=["Breakfast", "Lunch"],
                meal_type="main_course",
                attributes=["Rice", "Spicy", "Popular"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Duck Rice",
                description="Braised duck served with either plain rice or yam rice.",
                price=6.00,
                cuisine="Chinese",
                spiciness=0,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Rice"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Nasi Padang",
                description="Steamed rice served with a variety of pre-cooked dishes.",
                price=15.00,
                cuisine="Malay",
                spiciness=8,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Rice", "Spicy", "Variety"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Vegetarian Briyani",
                description=(
                    "Aromatic basmati rice cooked with mixed vegetables and spices."
                ),
                price=7.50,
                cuisine="Indian",
                spiciness=5,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Rice", "Vegetarian", "Healthy"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Economy Rice (Cai Fan)",
                description=(
                    "Plain rice with a selection of several cooked dishes. Price "
                    "varies."
                ),
                price=4.50,
                cuisine="Chinese",
                spiciness=3,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Rice", "Budget", "Variety"],
                is_halal=False,
                is_vegetarian=False,
            ),
            # === NOODLE-BASED MAINS ===
            Dish(
                name="Laksa",
                description=(
                    "Spicy noodle soup with coconut milk, shrimp, cockles, and "
                    "fishcake."
                ),
                price=6.00,
                cuisine="Local",
                spiciness=8,
                meal_time=["Lunch"],
                meal_type="main_course",
                attributes=["Soupy", "Spicy", "Noodles", "Popular", "Seafood"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Char Kway Teow",
                description=(
                    "Stir-fried flat rice noodles with dark soy sauce, shrimp, and "
                    "Chinese sausage."
                ),
                price=7.00,
                cuisine="Chinese",
                spiciness=3,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Noodles", "Popular"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Hokkien Mee",
                description=(
                    "Stir-fried yellow noodles and rice vermicelli with shrimp, "
                    "squid, and a rich prawn broth."
                ),
                price=8.00,
                cuisine="Chinese",
                spiciness=3,
                meal_time=["Dinner"],
                meal_type="main_course",
                attributes=["Noodles", "Seafood"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Bak Chor Mee",
                description=(
                    "Minced meat noodles, often with mushrooms, pork balls, and a "
                    "vinegar-based sauce."
                ),
                price=5.00,
                cuisine="Chinese",
                spiciness=4,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Noodles", "Popular"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Wonton Mee",
                description=(
                    "Egg noodles with barbecued pork (char siu) and wonton dumplings."
                ),
                price=5.00,
                cuisine="Chinese",
                spiciness=2,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Noodles"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Mee Rebus",
                description=(
                    "Yellow egg noodles in a thick, spicy, sweet potato-based gravy."
                ),
                price=4.50,
                cuisine="Malay",
                spiciness=5,
                meal_time=["Breakfast", "Lunch"],
                meal_type="main_course",
                attributes=["Noodles", "Spicy"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Mee Soto",
                description=(
                    "Spicy chicken noodle soup, often with shredded chicken and a "
                    "clear broth."
                ),
                price=5.00,
                cuisine="Malay",
                spiciness=6,
                meal_time=["Lunch"],
                meal_type="main_course",
                attributes=["Noodles", "Soupy", "Spicy"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Sliced Fish Bee Hoon",
                description="Rice vermicelli soup with slices of fresh fish.",
                price=6.50,
                cuisine="Chinese",
                spiciness=0,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Soupy", "Noodles", "Healthy"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Vegetarian Bee Hoon",
                description="Stir-fried rice vermicelli with vegetables.",
                price=4.50,
                cuisine="Chinese",
                spiciness=0,
                meal_time=["Breakfast", "Lunch"],
                meal_type="main_course",
                attributes=["Noodles", "Vegetarian"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Creamy Carbonara",
                description="Pasta with a creamy egg-based sauce, bacon, and cheese.",
                price=18.00,
                cuisine="Western",
                spiciness=0,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Pasta", "Comfort"],
                is_halal=False,
                is_vegetarian=False,
            ),
            # === FAMOUS MAINS & ZI CHAR ===
            Dish(
                name="Chilli Crab",
                description=(
                    "Mud crabs stir-fried in a sweet, savoury, and spicy "
                    "tomato-based sauce. A national dish."
                ),
                price=45.00,
                cuisine="Local",
                spiciness=7,
                meal_time=["Dinner"],
                meal_type="main_course",
                attributes=["Seafood", "Spicy", "Popular", "Splurge"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Fish Head Curry",
                description="A large fish head and vegetables cooked in a rich curry.",
                price=25.00,
                cuisine="Indian",
                spiciness=8,
                meal_time=["Lunch", "Dinner"],
                meal_type="main_course",
                attributes=["Spicy", "Seafood", "Splurge"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Bak Kut Teh",
                description="Porky rib soup boiled with herbs and spices.",
                price=12.00,
                cuisine="Chinese",
                spiciness=2,
                meal_time=["Dinner", "Supper"],
                meal_type="main_course",
                attributes=["Soupy", "Comfort"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Cereal Prawn",
                description="Deep-fried prawns coated in a buttery cereal mix.",
                price=22.00,
                cuisine="Chinese",
                spiciness=1,
                meal_time=["Dinner"],
                meal_type="side_dish",
                attributes=["Seafood", "Zi Char", "Splurge"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Sambal Kangkong",
                description="Water spinach stir-fried with spicy sambal sauce.",
                price=10.00,
                cuisine="Chinese",
                spiciness=8,
                meal_time=["Dinner"],
                meal_type="side_dish",
                attributes=["Vegetable", "Spicy", "Zi Char"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Hotplate Tofu",
                description="Sizzling plate of egg tofu with minced meat and sauce.",
                price=14.00,
                cuisine="Chinese",
                spiciness=2,
                meal_time=["Dinner"],
                meal_type="side_dish",
                attributes=["Tofu", "Zi Char"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Salted Egg Pork Ribs",
                description=(
                    "Fried pork ribs coated in a creamy and savoury salted egg yolk "
                    "sauce."
                ),
                price=18.00,
                cuisine="Chinese",
                spiciness=1,
                meal_time=["Dinner"],
                meal_type="side_dish",
                attributes=["Zi Char"],
                is_halal=False,
                is_vegetarian=False,
            ),
            # === BREADS, SNACKS & SIDES ===
            Dish(
                name="Roti Prata",
                description="South-Indian flatbread, served with fish or mutton curry.",
                price=3.50,
                cuisine="Indian",
                spiciness=6,
                meal_time=["Breakfast", "Supper"],
                meal_type="main_course",
                attributes=["Popular", "Budget"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Kaya Toast Set",
                description=(
                    "Toasted bread with coconut jam (kaya) and butter, served with "
                    "soft-boiled eggs and coffee."
                ),
                price=5.00,
                cuisine="Local",
                spiciness=0,
                meal_time=["Breakfast"],
                meal_type="main_course",
                attributes=["Popular", "Budget"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Murtabak",
                description=(
                    "Pan-fried bread stuffed with minced meat (mutton or chicken), "
                    "egg, and onion."
                ),
                price=9.00,
                cuisine="Indian",
                spiciness=4,
                meal_time=["Dinner"],
                meal_type="main_course",
                attributes=["Popular"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Thosai (Dosa)",
                description=(
                    "A thin pancake made from fermented rice batter, served with "
                    "chutneys and sambar."
                ),
                price=4.00,
                cuisine="Indian",
                spiciness=4,
                meal_time=["Breakfast", "Lunch"],
                meal_type="main_course",
                attributes=["Healthy", "Vegetarian"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Satay",
                description=(
                    "Grilled meat skewers served with peanut sauce, onions, and "
                    "cucumber."
                ),
                price=10.00,
                cuisine="Malay",
                spiciness=1,
                meal_time=["Dinner", "Supper"],
                meal_type="side_dish",
                attributes=["Popular", "Grilled"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Carrot Cake (Chai Tow Kway)",
                description=(
                    "Stir-fried radish cake cubes with eggs. Available in 'white' or "
                    "'black'."
                ),
                price=4.00,
                cuisine="Chinese",
                spiciness=1,
                meal_time=["Breakfast", "Lunch"],
                meal_type="main_course",
                attributes=["Popular"],
                is_halal=False,
                is_vegetarian=True,
            ),
            Dish(
                name="Oyster Omelette (Orh Luak)",
                description=(
                    "Starch-based omelette with fresh oysters, fried until crispy."
                ),
                price=8.50,
                cuisine="Local",
                spiciness=2,
                meal_time=["Dinner"],
                meal_type="main_course",
                attributes=["Seafood"],
                is_halal=False,
                is_vegetarian=False,
            ),
            Dish(
                name="Curry Puff",
                description=(
                    "A baked or fried pastry filled with curried potatoes, chicken, "
                    "and egg."
                ),
                price=2.00,
                cuisine="Local",
                spiciness=5,
                meal_time=["Any"],
                meal_type="snack",
                attributes=["Pastry", "Spicy"],
                is_halal=True,
                is_vegetarian=False,
            ),
            Dish(
                name="Chwee Kueh",
                description=(
                    "Steamed rice cakes topped with preserved radish (chai poh)."
                ),
                price=2.50,
                cuisine="Chinese",
                spiciness=2,
                meal_time=["Breakfast"],
                meal_type="snack",
                attributes=["Budget"],
                is_halal=False,
                is_vegetarian=True,
            ),
            # === DESSERTS & DRINKS ===
            Dish(
                name="Ice Kacang",
                description=(
                    "A mound of shaved ice topped with sweet syrups, red beans, "
                    "sweet corn, and attap chee."
                ),
                price=3.00,
                cuisine="Local",
                spiciness=0,
                meal_time=["Any"],
                meal_type="dessert",
                attributes=["Dessert", "Cold"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Chendol",
                description=(
                    "A dessert with pandan-flavored jelly noodles, coconut milk, and "
                    "palm sugar (gula melaka)."
                ),
                price=3.50,
                cuisine="Local",
                spiciness=0,
                meal_time=["Any"],
                meal_type="dessert",
                attributes=["Dessert", "Cold", "Popular"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Tau Huay (Soya Beancurd)",
                description=(
                    "Silken soya beancurd, served warm or cold with sugar syrup."
                ),
                price=2.00,
                cuisine="Chinese",
                spiciness=0,
                meal_time=["Any"],
                meal_type="dessert",
                attributes=["Dessert", "Healthy"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Teh Tarik",
                description="Hot 'pulled' milk tea with a frothy top.",
                price=1.80,
                cuisine="Local",
                spiciness=0,
                meal_time=["Any"],
                meal_type="drink",
                attributes=["Drink", "Hot"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Kopi-O",
                description="Traditional black coffee with sugar.",
                price=1.50,
                cuisine="Local",
                spiciness=0,
                meal_time=["Any"],
                meal_type="drink",
                attributes=["Drink", "Hot", "Budget"],
                is_halal=True,
                is_vegetarian=True,
            ),
            Dish(
                name="Sugarcane Juice",
                description=(
                    "Freshly squeezed sugarcane juice, often served with a lemon."
                ),
                price=2.50,
                cuisine="Local",
                spiciness=0,
                meal_time=["Any"],
                meal_type="drink",
                attributes=["Drink", "Cold", "Healthy"],
                is_halal=True,
                is_vegetarian=True,
            ),
        ]

        for dish in dishes:
            session.add(dish)
        session.commit()
        print(f"Successfully seeded database with {len(dishes)} Singapore dishes.")
        print("Ready to serve recommendations!")
        print("=" * 50)
