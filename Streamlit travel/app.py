# ================================================================
# PART–1 → Imports + CSS + JS + Data
# ================================================================

import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
from datetime import datetime
import os
import qrcode
from io import BytesIO

# ---------- Page Config ----------
st.set_page_config(
    page_title="TravelExplorer — Premium",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB = "travel.db"

# ---------- PREMIUM CSS + CAROUSEL JS ----------
UI_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');
* { font-family: 'Poppins', sans-serif !important; }

/* Background */
[data-testid="stAppViewContainer"] > .main {
  background: linear-gradient(180deg,#f4f7ff 0%, #ffffff 60%);
  padding: 20px 28px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#6a11cb,#2575fc);
  padding: 20px;
  color: white;
  border-radius: 12px;
}

/* Hero Banner */
.hero-banner {
  background: linear-gradient(90deg,#6a11cb,#2575fc);
  padding: 42px 30px;
  color: white;
  border-radius: 16px;
  margin-bottom: 22px;
  box-shadow: 0 12px 32px rgba(0,0,0,0.20);
}
.hero-banner h1 { font-size: 40px; font-weight: 900; margin: 0; }

/* Destination Cards */
.dest-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 26px;
  box-shadow: 0 12px 32px rgba(0,0,0,0.15);
  transition: 0.35s ease;
}
.dest-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 18px 40px rgba(0,0,0,0.22);
}
.dest-img {
  width: 100%; height: 320px; object-fit: cover;
}
.dest-gradient {
  position: absolute; bottom: 0; left: 0;
  width: 100%; height: 50%;
  background: linear-gradient(to top, rgba(0,0,0,0.85), rgba(0,0,0,0));
}
.city-text {
  position: absolute; left: 22px; bottom: 60px;
  color: white; font-size: 34px; font-weight: 900;
  text-shadow: 0 6px 18px rgba(0,0,0,0.8);
}
.city-sub {
  position: absolute; left: 22px; bottom: 26px;
  color: rgba(255,255,255,0.90); font-size: 15px;
}

/* Grid */
.grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }

/* Carousel */
.home-carousel { position:relative; overflow:hidden; border-radius:16px; margin-bottom:20px; }
.home-carousel-track { display:flex; transition:transform .7s cubic-bezier(.2,.9,.2,1); }
.home-slide img { width:100%; height:370px; object-fit:cover; border-radius:14px; }
.home-slide { min-width:100%; position:relative; }
.home-slide-text {
  position:absolute; left:26px; bottom:22px;
  color:white; font-weight:900; font-size:34px;
  text-shadow:0 8px 20px rgba(0,0,0,0.75);
}
</style>

<script>
window.addEventListener("load", function(){
  const car = document.querySelector("#homeCarousel");
  if(!car) return;
  const track = car.querySelector(".home-carousel-track");
  const slides = car.querySelectorAll(".home-slide");
  let idx=0;
  function go(n){ idx=(n+slides.length)%slides.length;
    track.style.transform = `translateX(-${idx*100}%)`; }
  setInterval(()=>go(idx+1), 4000);
});
</script>
"""

st.markdown(UI_CSS, unsafe_allow_html=True)

# --------------------------- DESTINATIONS DATA ----------------------------
DESTS = [
    {"name":"Goa","country":"India","price":15000,"cat":"Beach","img":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e","lat":15.2993,"lon":74.1240},
    {"name":"Manali","country":"India","price":18000,"cat":"Snow • Hills","img":"https://images.unsplash.com/photo-1482192505345-5655af888cc4","lat":32.2396,"lon":77.1887},
    {"name":"Jaipur","country":"India","price":12000,"cat":"Heritage","img":"https://images.unsplash.com/photo-1548013146-72479768bada","lat":26.9124,"lon":75.7873},
    {"name":"Kerala","country":"India","price":22000,"cat":"Backwaters","img":"https://images.unsplash.com/photo-1501436513145-30f24e19fcc8","lat":10.8505,"lon":76.2711},
    {"name":"Dubai","country":"UAE","price":110000,"cat":"Luxury","img":"https://images.unsplash.com/photo-1534237710431-e2fc698436d0","lat":25.2048,"lon":55.2708},
    {"name":"Paris","country":"France","price":120000,"cat":"Romantic","img":"https://images.unsplash.com/photo-1502602898657-3e91760cbb34","lat":48.8566,"lon":2.3522},
    {"name":"London","country":"UK","price":130000,"cat":"Royal • Modern","img":"https://images.unsplash.com/photo-1469474968028-56623f02e42e","lat":51.5072,"lon":-0.1276},
    {"name":"Tokyo","country":"Japan","price":140000,"cat":"Tech • Culture","img":"https://images.unsplash.com/photo-1549692520-acc6669e2f0c?q=80&w=1080","lat":35.6762,"lon":139.6503},
    {"name":"Sydney","country":"Australia","price":160000,"cat":"Beaches • Lifestyle","img":"https://images.unsplash.com/photo-1506976785307-8732e854ad89?auto=format&fit=crop&w=1080&q=80","lat":-33.8688,"lon":151.2093},
]
# ================================================================
# PART–2 → DB INITIALIZATION, AUTH, HELPERS, PRICING, PDF GENERATOR
# (Paste this right after PART–1)
# ================================================================

# -----------------------
# Additional data (hotels, packages, pricing overrides)
# -----------------------
HOTEL_SPECIFIC_PRICING = {
    "Goa": {"Deluxe": 4000, "Suite": 6500, "Pool View": 9000},
    "Paris": {"Deluxe": 18000, "Suite": 26000, "Pool View": 32000},
    "Dubai": {"Deluxe": 22000, "Suite": 35000, "Pool View": 50000},
}

HOTELS = {
    "Goa": {"name": "Taj Holiday Village Resort", "rating": 4.7, "price": 8500,
            "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"},
    "Manali": {"name": "Snow Valley Resorts", "rating": 4.5, "price": 6000,
               "img": "https://images.unsplash.com/photo-1482192505345-5655af888cc4"},
    "Jaipur": {"name": "Rambagh Palace", "rating": 4.9, "price": 12000,
               "img": "https://images.unsplash.com/photo-1548013146-72479768bada"},
    "Mumbai": {"name": "The Taj Mahal Palace", "rating": 4.8, "price": 11000,
               "img": "https://images.unsplash.com/photo-1528701800489-20be3c2a27e9"},
    "Kerala": {"name": "Kumarakom Lake Resort", "rating": 4.7, "price": 9000,
               "img": "https://images.unsplash.com/photo-1505691938895-1758d7feb511"},
    "Dubai": {"name": "Burj Al Arab Jumeirah", "rating": 5.0, "price": 45000,
             "img": "https://images.unsplash.com/photo-1534237710431-e2fc698436d0"},
    "Paris": {"name": "Hôtel Plaza Athénée", "rating": 4.8, "price": 25000,
              "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"},
}

PACKAGES = [
    {"title":"Goa Beach Fun","days":3,"price":14000,"tag":"10% OFF","img":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e"},
    {"title":"Manali Snow Adventure","days":5,"price":22000,"tag":"Breakfast Free","img":"https://images.unsplash.com/photo-1482192505345-5655af888cc4"},
    {"title":"Royal Rajasthan Tour","days":4,"price":20000,"tag":"Heritage Special","img":"https://images.unsplash.com/photo-1548013146-72479768bada"},
    {"title":"Kerala Backwater Luxury","days":5,"price":35000,"tag":"Houseboat Stay","img":"https://images.unsplash.com/photo-1501436513145-30f24e19fcc8"},
    {"title":"Paris Romantic Getaway","days":6,"price":125000,"tag":"Free Cruise","img":"https://images.unsplash.com/photo-1502602898657-3e91760cbb34"},
]

# -----------------------
# Default room pricing (Option 1)
# -----------------------
DEFAULT_ROOM_PRICES = {
    "Deluxe": 3500,
    "Suite": 5500,
    "Pool View": 7000,
}
BREAKFAST_PER_PERSON_PER_DAY = 500
GST_PERCENT = 12.0

# -----------------------
# DB AUTO-MIGRATION / Initialization
# -----------------------
def get_existing_columns(conn, table_name):
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table_name})")
    rows = c.fetchall()
    return [r[1] for r in rows]

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # ensure users table exists
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

    # If bookings table does not exist, create full schema
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
    exists = c.fetchone()
    if not exists:
        c.execute('''CREATE TABLE bookings (
            id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            type TEXT,
            destination TEXT,
            hotel_name TEXT,
            room_type TEXT,
            rooms INTEGER,
            nights INTEGER,
            people INTEGER,
            breakfast INTEGER,
            base_amount REAL,
            gst REAL,
            total_amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
        return

    # bookings table exists -> check columns and add missing ones
    existing = get_existing_columns(conn, "bookings")
    desired = {
        "type": ("TEXT", "'general'"),
        "destination": ("TEXT", "''"),
        "hotel_name": ("TEXT", "''"),
        "room_type": ("TEXT", "''"),
        "rooms": ("INTEGER", "0"),
        "nights": ("INTEGER", "0"),
        "people": ("INTEGER", "0"),
        "breakfast": ("INTEGER", "0"),
        "base_amount": ("REAL", "0"),
        "gst": ("REAL", "0"),
        "total_amount": ("REAL", "0"),
        "timestamp": ("DATETIME", "CURRENT_TIMESTAMP")
    }
    for col, (sqltype, default) in desired.items():
        if col not in existing:
            try:
                c.execute(f"ALTER TABLE bookings ADD COLUMN {col} {sqltype} DEFAULT {default}")
            except Exception:
                pass
    conn.commit()
    conn.close()

# initialize DB
init_db()

# -----------------------
# Auth helpers
# -----------------------
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def add_user(username, password):
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_pw(password)))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def verify_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return (row and row[0] == hash_pw(password))

# -----------------------
# Booking save / fetch helpers
# -----------------------
def save_hotel_booking(record: dict):
    """
    record keys:
    username,name,destination,hotel_name,room_type,rooms,nights,people,breakfast,base_amount,gst,total_amount
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        """INSERT INTO bookings (
            username, name, type, destination, hotel_name,
            room_type, rooms, nights, people, breakfast,
            base_amount, gst, total_amount
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            record["username"],
            record["name"],
            "hotel",
            record["destination"],
            record["hotel_name"],
            record["room_type"],
            int(record["rooms"]),
            int(record["nights"]),
            int(record["people"]),
            int(record["breakfast"]),
            float(record["base_amount"]),
            float(record["gst"]),
            float(record["total_amount"])
        )
    )
    booking_id = c.lastrowid
    conn.commit()
    # fetch timestamp
    c.execute("SELECT timestamp FROM bookings WHERE id=?", (booking_id,))
    ts = c.fetchone()[0]
    conn.close()
    return booking_id, ts

def save_general_booking(username, name, dest, people, est):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""INSERT INTO bookings (
                    username, name, type, destination, hotel_name, room_type, rooms, nights, people, breakfast, base_amount, gst, total_amount
                 ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
              (username, name, "general", dest, "", "", 0, 0, int(people), 0, float(est), 0.0, float(est)))
    booking_id = c.lastrowid
    conn.commit()
    c.execute("SELECT timestamp FROM bookings WHERE id=?", (booking_id,))
    ts = c.fetchone()[0]
    conn.close()
    return booking_id, ts

def get_user_bookings(username):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM bookings WHERE username=? ORDER BY timestamp DESC", conn, params=(username,))
    conn.close()
    return df

# -----------------------
# Pricing utilities
# -----------------------
def get_room_price_for_hotel(destination_name, room_type):
    hotel_prices = HOTEL_SPECIFIC_PRICING.get(destination_name)
    if hotel_prices and room_type in hotel_prices:
        return hotel_prices[room_type]
    return DEFAULT_ROOM_PRICES.get(room_type, DEFAULT_ROOM_PRICES["Deluxe"])

def calc_hotel_cost(destination_name, room_type, rooms, nights, people, breakfast_selected):
    per_room_per_night = get_room_price_for_hotel(destination_name, room_type)
    rooms_cost = per_room_per_night * rooms * nights
    breakfast_cost = 0
    if breakfast_selected:
        breakfast_cost = BREAKFAST_PER_PERSON_PER_DAY * people * nights
    base_amount = rooms_cost + breakfast_cost
    gst = (GST_PERCENT / 100.0) * base_amount
    total = base_amount + gst
    return {
        "per_room_per_night": int(per_room_per_night),
        "rooms_cost": int(rooms_cost),
        "breakfast_cost": int(breakfast_cost),
        "base_amount": int(base_amount),
        "gst": round(gst, 2),
        "total_amount": round(total, 2)
    }

# -----------------------
# PDF Voucher generator (hotel + ticket + QR + grand total)
# -----------------------
def generate_hotel_voucher_pdf(hotel_record: dict, ticket_record: dict = None):
    """
    hotel_record = hotel booking dict
    ticket_record = general booking dict (optional)
    Generates combined PDF + QR + Grand Total
    """
    # Prepare QR text
    qr_text = f"Booking ID: {hotel_record.get('id')} | Name: {hotel_record.get('name')} | Destination: {hotel_record.get('destination')} | Hotel: {hotel_record.get('hotel_name')} | Total: Rs. {hotel_record.get('total_amount')} | Time: {hotel_record.get('timestamp')}"
    qr_img = qrcode.make(qr_text)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_bytes = qr_buffer.getvalue()

    # Start PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Header / title
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(255, 56, 92)
    pdf.cell(0, 10, "TravelExplorer - Combined Voucher", ln=True, align='C')
    pdf.ln(4)

    # Save temp QR file
    qr_file = "qr_temp.png"
    try:
        with open(qr_file, "wb") as f:
            f.write(qr_bytes)
        pdf.image(qr_file, x=160, y=15, w=35)
    except Exception:
        # If image insertion fails, continue without QR
        pass

    # HOTEL SECTION
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "HOTEL SECTION", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.ln(2)
    pdf.cell(0, 7, f"Hotel Name: {hotel_record.get('hotel_name')}", ln=True)
    pdf.cell(0, 7, f"Destination: {hotel_record.get('destination')}", ln=True)
    pdf.cell(0, 7, f"Room Type: {hotel_record.get('room_type')}", ln=True)
    pdf.cell(0, 7, f"Rooms: {hotel_record.get('rooms')} | Nights: {hotel_record.get('nights')}", ln=True)
    pdf.cell(0, 7, f"People: {hotel_record.get('people')}", ln=True)
    pdf.cell(0, 7, f"Breakfast: {'Yes' if hotel_record.get('breakfast') else 'No'}", ln=True)
    pdf.ln(3)
    pdf.cell(0, 7, f"Base Amount: Rs. {hotel_record.get('base_amount')}", ln=True)
    pdf.cell(0, 7, f"GST ({GST_PERCENT}%): Rs. {hotel_record.get('gst')}", ln=True)
    pdf.cell(0, 7, f"Total Hotel Amount: Rs. {hotel_record.get('total_amount')}", ln=True)
    pdf.ln(8)

    # TRAVEL TICKET SECTION
    ticket_total = 0
    if ticket_record:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, "TRAVEL TICKET SECTION", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.ln(2)
        pdf.cell(0, 7, f"Destination: {ticket_record.get('destination')}", ln=True)
        pdf.cell(0, 7, f"Ticket Price: Rs. {ticket_record.get('base_amount')}", ln=True)
        pdf.cell(0, 7, f"People: {ticket_record.get('people')}", ln=True)
        pdf.cell(0, 7, f"Total Ticket Cost: Rs. {ticket_record.get('total_amount')}", ln=True)
        ticket_total = ticket_record.get("total_amount", 0)
        pdf.ln(8)

    # GRAND TOTAL
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "GRAND TOTAL", ln=True)
    hotel_total = hotel_record.get("total_amount", 0)
    grand = (hotel_total or 0) + (ticket_total or 0)
    pdf.set_font("Arial", "", 12)
    pdf.ln(2)
    pdf.cell(0, 7, f"Hotel Amount: Rs. {hotel_total}", ln=True)
    pdf.cell(0, 7, f"Ticket Amount: Rs. {ticket_total}", ln=True)
    pdf.cell(0, 7, f"----------------------------------------", ln=True)
    pdf.cell(0, 8, f"GRAND TOTAL PAYABLE: Rs. {grand}", ln=True)

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 6, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    # Cleanup QR temp
    try:
        if os.path.exists(qr_file):
            os.remove(qr_file)
    except:
        pass

    return pdf.output(dest='S').encode('latin-1')

# -----------------------
# Part-2 complete
# -----------------------
# ================================================================
# PART–3 → Navigation + Home (Premium UI) + Destinations
# ================================================================

# ---------------------------------
# Sidebar Navigation
# ---------------------------------
st.sidebar.title("✈️ TravelExplorer")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Destinations", "Hotel Booking", "Packages", "Booking (general)", "Bookings", "Login/Signup"]
)

# Maintain login state
if "user" not in st.session_state:
    st.session_state["user"] = None


# ================================================================
# LOGIN / SIGNUP PAGE
# ================================================================
if page == "Login/Signup":
    st.markdown("<h2>🔐 Login / Signup</h2>", unsafe_allow_html=True)

    mode = st.radio("Choose Mode", ["Login", "Signup"], horizontal=True)

    if mode == "Signup":
        su = st.text_input("Create Username")
        sp = st.text_input("Create Password", type="password")
        if st.button("Create Account"):
            if not su or not sp:
                st.error("Enter valid username & password")
            elif add_user(su, sp):
                st.success("Account created successfully! Now login.")
            else:
                st.error("Username already exists.")
    else:
        lu = st.text_input("Username")
        lp = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_user(lu, lp):
                st.success("Login successful!")
                st.session_state["user"] = lu
            else:
                st.error("Invalid username/password")


# ================================================================
# HOME PAGE — PREMIUM DESIGN
# ================================================================
elif page == "Home":

    # ---------- HERO BANNER ----------
    st.markdown("""
        <div class='hero-banner'>
            <h1>🌍 TravelExplorer — Premium Experience</h1>
            <p>Book hotels, explore destinations, generate QR vouchers — all in one place.</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------- CATEGORY SHORTCUT BUTTONS ----------
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='cat-btn'>🏖 Beaches</div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='cat-btn'>🏔 Adventure</div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='cat-btn'>🏙 City</div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='cat-btn'>💑 Honeymoon</div>", unsafe_allow_html=True)

    # ---------- AUTO-SLIDING CAROUSEL ----------
    st.markdown("<div class='home-carousel' id='homeCarousel'>", unsafe_allow_html=True)
    st.markdown("<div class='home-carousel-track'>", unsafe_allow_html=True)

    for d in DESTS[:6]:  # first 6 destinations
        st.markdown(f"""
            <div class='home-slide'>
                <img src="{d['img']}" />
                <div class='home-slide-text'>{d['name']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------- TRENDING DESTINATIONS ----------
    st.markdown("<h2 style='margin-top:20px;'>🔥 Trending Destinations</h2>", unsafe_allow_html=True)

    st.markdown("<div class='grid-3'>", unsafe_allow_html=True)

    for d in DESTS:
        st.markdown(f"""
            <div class='dest-card'>
                <img class='dest-img' src="{d['img']}">
                <div class='dest-gradient'></div>
                <div class='city-text'>{d['name']}</div>
                <div class='city-sub'>{d['country']} • {d['cat']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# DESTINATIONS PAGE — PREMIUM DESIGN
# ================================================================
elif page == "Destinations":
    st.markdown("<h1>📍 Explore All Destinations</h1>", unsafe_allow_html=True)

    st.markdown("<div class='grid-3'>", unsafe_allow_html=True)

    for d in DESTS:
        st.markdown(f"""
            <div class='dest-card'>
                <img class='dest-img' src="{d['img']}">

                <div class='dest-gradient'></div>

                <div class='city-text'>{d['name']}</div>

                <div class='city-sub'>{d['country']} • {d['cat']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
# ================================================================
# PART–4 → Hotel Booking + Packages + General Booking + Bookings
# (Paste this after PART–3)
# ================================================================

# -----------------------
# HOTEL BOOKING (Premium layout)
# -----------------------
if page == "Hotel Booking":
    st.markdown("<h1>🏨 Hotel Booking (Premium)</h1>", unsafe_allow_html=True)

    if not st.session_state.get("user"):
        st.warning("Please login first (Login/Signup in sidebar).")
    else:
        user = st.session_state["user"]

        left, right = st.columns([2, 1])
        with left:
            dest_choice = st.selectbox("Choose destination / city", [d["name"] for d in DESTS], index=0)
            hotel_meta = HOTELS.get(dest_choice)
            if hotel_meta:
                st.markdown(
                    f"<div class='card'><img src='{hotel_meta['img']}' style='width:100%; border-radius:12px;' /></div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='display:flex; gap:12px; margin-top:10px;'>"
                    f"<div class='card' style='flex:1'><strong style='font-size:18px'>{hotel_meta['name']}</strong>"
                    f"<div class='small-muted'>⭐ {hotel_meta['rating']} • Rs. {hotel_meta['price']} per night (info)</div></div>"
                    f"<div class='card' style='width:180px; text-align:center'><div style='font-weight:800; color:#6a11cb; font-size:18px'>Special</div>"
                    f"<div class='small-muted'>Seasonal rates</div></div></div>",
                    unsafe_allow_html=True
                )
            else:
                st.info("No hotel info available for this destination.")

            # hotel gallery (3 thumbnails)
            if hotel_meta:
                gcols = st.columns(3)
                for i in range(3):
                    with gcols[i]:
                        st.image(hotel_meta["img"], use_column_width=True, caption=f"{hotel_meta['name']}")

        with right:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Booking Details")
            guest_name = st.text_input("Guest full name", key="hb_guest")
            room_type = st.selectbox("Room type", ["Deluxe", "Suite", "Pool View"], key="hb_room")
            rooms = st.number_input("Number of rooms", min_value=1, max_value=10, value=1, key="hb_rooms")
            nights = st.number_input("Number of nights", min_value=1, max_value=30, value=1, key="hb_nights")
            people = st.number_input("Total people", min_value=1, max_value=20, value=1, key="hb_people")
            breakfast = st.checkbox(f"Add breakfast (Rs. {BREAKFAST_PER_PERSON_PER_DAY}/person/day)", value=False, key="hb_breakfast")

            # compute pricing
            pricing = calc_hotel_cost(dest_choice, room_type, rooms, nights, people, breakfast)
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.write(f"Per room / night: Rs. {pricing['per_room_per_night']}")
            st.write(f"Rooms cost (rooms × nights): Rs. {pricing['rooms_cost']}")
            st.write(f"Breakfast cost: Rs. {pricing['breakfast_cost']}")
            st.write(f"Base amount: Rs. {pricing['base_amount']}")
            st.write(f"GST ({GST_PERCENT}%): Rs. {pricing['gst']}")
            st.markdown(f"## Grand Total: Rs. {pricing['total_amount']}")
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("Confirm Hotel Booking"):
                if not guest_name.strip():
                    st.error("Enter guest name.")
                else:
                    rec = {
                        "username": user,
                        "name": guest_name.strip(),
                        "destination": dest_choice,
                        "hotel_name": hotel_meta['name'] if hotel_meta else dest_choice,
                        "room_type": room_type,
                        "rooms": int(rooms),
                        "nights": int(nights),
                        "people": int(people),
                        "breakfast": int(breakfast),
                        "base_amount": pricing['base_amount'],
                        "gst": pricing['gst'],
                        "total_amount": pricing['total_amount']
                    }
                    booking_id, ts = save_hotel_booking(rec)
                    st.success(f"✅ Hotel booking saved! Booking ID: {booking_id}")

                    # Prepare voucher record
                    voucher_record = rec.copy()
                    voucher_record["id"] = booking_id
                    voucher_record["timestamp"] = ts

                    # find latest general booking (ticket) for user (if any)
                    ticket_df = get_user_bookings(user)
                    ticket_df = ticket_df[ticket_df["type"] == "general"]
                    ticket_record = ticket_df.iloc[0].to_dict() if not ticket_df.empty else None

                    pdf_bytes = generate_hotel_voucher_pdf(voucher_record, ticket_record)

                    st.download_button(
                        label="Download Combined Voucher (PDF)",
                        data=pdf_bytes,
                        file_name=f"voucher_{booking_id}.pdf",
                        mime="application/pdf"
                    )

# -----------------------
# PACKAGES
# -----------------------
elif page == "Packages":
    st.markdown("<h1>🎁 Popular Packages</h1>", unsafe_allow_html=True)
    st.markdown("<div class='grid-3'>", unsafe_allow_html=True)
    for p in PACKAGES:
        st.markdown(f"""
            <div class='card'>
                <img src="{p['img']}" style="width:100%; height:160px; object-fit:cover; border-radius:10px" />
                <div style='display:flex;justify-content:space-between;align-items:center;margin-top:10px'>
                    <div><strong>{p['title']}</strong><div class='small-muted'>{p['days']} days • {p['tag']}</div></div>
                    <div><span style='background:linear-gradient(90deg,#ff8a00,#e52e71);color:white;padding:6px 12px;border-radius:999px;font-weight:700;'>Rs. {p['price']}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# GENERAL BOOKING (old flow)
# -----------------------
elif page == "Booking (general)":
    st.markdown("<h1>📝 General Booking</h1>", unsafe_allow_html=True)
    if not st.session_state.get("user"):
        st.info("Login to use general booking.")
    else:
        user = st.session_state["user"]
        name = st.text_input("Your name for booking", key="gen_name")
        dest = st.selectbox("Destination", [d["name"] for d in DESTS], key="gen_dest")
        people = st.number_input("People", min_value=1, max_value=20, value=1, key="gen_people")
        price = next((d["price"] for d in DESTS if d["name"] == dest), 0)
        est = price * people
        st.write(f"Estimated Price: Rs. {est}")
        if st.button("Confirm general booking"):
            booking_id, ts = save_general_booking(user, name, dest, people, est)
            st.success(f"General booking saved! Booking ID: {booking_id}")

# -----------------------
# BOOKINGS LIST (Dashboard) + Voucher download
# -----------------------
elif page == "Bookings":
    st.markdown("<h1>📄 My Bookings</h1>", unsafe_allow_html=True)

    if not st.session_state.get("user"):
        st.info("Please login to view your bookings.")
    else:
        user = st.session_state["user"]
        df = get_user_bookings(user)
        if df.empty:
            st.info("You have no bookings yet.")
        else:
            # Show summary cards (latest 3)
            recent = df.head(3)
            cols = st.columns(len(recent))
            for i, (_, r) in enumerate(recent.iterrows()):
                with cols[i]:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"**#{int(r['id'])} — {r.get('type','general').title()}**", unsafe_allow_html=True)
                    st.markdown(f"<div class='small-muted'>{r.get('destination','')} • On: {r.get('timestamp','')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<strong>Rs. {r.get('total_amount',0)}</strong>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<hr/>", unsafe_allow_html=True)

            # Full list
            for _, row in df.iterrows():
                st.markdown("<div class='card' style='margin-bottom:12px;'>", unsafe_allow_html=True)
                typ = row.get("type", "general")
                left_col, right_col = st.columns([3,1])
                with left_col:
                    st.markdown(
                        f"**Booking ID:** {row['id']}  •  **Type:** {typ.title()}  \n\n"
                        f"**Name:** {row.get('name','')}  \n\n"
                        f"**Destination:** {row.get('destination','')}  \n\n"
                        f"**Hotel:** {row.get('hotel_name','')}  \n\n"
                        f"**People:** {row.get('people',0)}",
                        unsafe_allow_html=True
                    )
                with right_col:
                    st.markdown(f"<div style='text-align:right'><strong>Rs. {row.get('total_amount',0)}</strong><div class='small-muted'>On: {row.get('timestamp','')}</div></div>", unsafe_allow_html=True)

                    if typ == "hotel":
                        record = {
                            "id": row["id"],
                            "username": row["username"],
                            "name": row["name"],
                            "destination": row["destination"],
                            "hotel_name": row["hotel_name"],
                            "room_type": row["room_type"],
                            "rooms": int(row["rooms"]),
                            "nights": int(row["nights"]),
                            "people": int(row["people"]),
                            "breakfast": int(row["breakfast"]),
                            "base_amount": row["base_amount"],
                            "gst": row["gst"],
                            "total_amount": row["total_amount"],
                            "timestamp": row["timestamp"]
                        }
                        # find associated latest general ticket if any
                        ticket_df = get_user_bookings(row["username"])
                        ticket_df = ticket_df[ticket_df["type"] == "general"]
                        ticket_record = ticket_df.iloc[0].to_dict() if not ticket_df.empty else None

                        pdf_bytes = generate_hotel_voucher_pdf(record, ticket_record)
                        st.download_button(f"Download voucher #{row['id']}", data=pdf_bytes, file_name=f"voucher_{row['id']}.pdf", mime="application/pdf")
                st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Fallback (safety) - shouldn't happen
# -----------------------
else:
    st.info("Select a page from the sidebar.")
