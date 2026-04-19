import os
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st

PRODUCTS_FILE = "products.csv"
GST_RATE = 0.18

DEFAULT_PRODUCTS = [
    {"Product Name": "DVR 8 Channel (CP Plus)", "Price": 4250},
    {"Product Name": "Dome Camera (Mic + Color)", "Price": 1650},
    {"Product Name": "Bullet Camera (Mic + Color)", "Price": 1750},
    {"Product Name": "HDD 1TB", "Price": 6350},
    {"Product Name": "Power Supply (Other Brand)", "Price": 750},
    {"Product Name": "DC/BNC Connector", "Price": 60},
    {"Product Name": "Camera Box / Junction Box", "Price": 60},
    {"Product Name": "3+1 Wire (Other Brand)", "Price": 950},
    {"Product Name": "2U Rack", "Price": 800},
    {"Product Name": "Installation", "Price": 1500},
]

def ensure_products_file():
    # just in case it doesn't exist
    if not os.path.exists(PRODUCTS_FILE):
        pd.DataFrame(DEFAULT_PRODUCTS).to_csv(PRODUCTS_FILE, index=False)
        return

    df = pd.read_csv(PRODUCTS_FILE)
    if not {"Product Name", "Price"}.issubset(df.columns):
        pd.DataFrame(DEFAULT_PRODUCTS).to_csv(PRODUCTS_FILE, index=False)

def load_products():
    ensure_products_file()
    df = pd.read_csv(PRODUCTS_FILE)
    df["Product Name"] = df["Product Name"].astype(str).str.strip()
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Price"])
    df = df[df["Product Name"] != ""]
    df = df.drop_duplicates(subset=["Product Name"], keep="first")
    return df.sort_values("Product Name").reset_index(drop=True)

def add_product(name, price):
    name = name.strip()
    if not name:
        return False, "Product name is required."
    if price <= 0:
        return False, "Price must be greater than 0."

    df = load_products()
    existing = set(df["Product Name"].str.lower().str.strip())
    if name.lower() in existing:
        return False, "Product already exists."

    new_row = pd.DataFrame([{"Product Name": name, "Price": float(price)}])
    df = pd.concat([df, new_row], ignore_index=True)
    df = df.drop_duplicates(subset=["Product Name"], keep="first")
    df = df.sort_values("Product Name").reset_index(drop=True)
    df.to_csv(PRODUCTS_FILE, index=False)
    return True, "Product added successfully."

def delete_product(name):
    df = load_products()
    df = df[df["Product Name"] != name]
    df.to_csv(PRODUCTS_FILE, index=False)
    return True

def init_state():
    if "cart" not in st.session_state:
        st.session_state.cart = []
    
    if "invoice_no" not in st.session_state:
        st.session_state.invoice_no = f"EST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

def calc_totals(items):
    subtotal = float(sum(item["total"] for item in items))
    gst = subtotal * GST_RATE
    return subtotal, subtotal + gst

def build_wa_link(phone, name, inv_no, inv_date, items, subtotal, gst, total):
    
    phone_raw = "".join(ch for ch in phone if ch.isdigit())
    
    # default to indian code
    if not phone_raw.startswith("91") and len(phone_raw) == 10:
        phone_raw = "91" + phone_raw

    msg = f"*Estimate from RAJU DWIVEDI*\n"
    msg += f"Customer: {name}\n"
    msg += f"Estimate No: {inv_no}\n"
    msg += f"Date: {inv_date}\n\n*Items:*\n"
    
    for item in items:
        msg += f"- {item['product']} (x{item['qty']}): Rs {item['total']:.2f}\n"

    msg += f"\nSubtotal: Rs {subtotal:.2f}\n"
    msg += f"GST ({int(GST_RATE*100)}%): Rs {gst:.2f}\n"
    msg += f"*Grand Total: Rs {total:.2f}*\n\n"
    msg += "Thank you for your business!"

    return f"https://wa.me/{phone_raw}?text={quote(msg)}"

def main():
    st.set_page_config(page_title="Billing & WhatsApp Estimate", page_icon="🧾", layout="wide")
    init_state()

    st.title("Billing & WhatsApp Estimate System")

    df = load_products()
    price_map = {row["Product Name"]: float(row["Price"]) for _, row in df.iterrows()}
    options = list(price_map.keys())

    with st.sidebar:
        st.subheader("Add Product to Catalog")
        with st.form("add_product_form", clear_on_submit=True):
            new_name = st.text_input("Product Name")
            new_price = st.number_input("Price", min_value=0.0, step=10.0, format="%.2f")
            
            if st.form_submit_button("Add Product"):
                ok, msg = add_product(new_name, float(new_price))
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.subheader("Remove Product")
        with st.form("rm_product_form", clear_on_submit=True):
            del_product = st.selectbox("Select Product to Delete", options)
            if st.form_submit_button("Delete"):
                if delete_product(del_product):
                    st.success(f"{del_product} deleted.")
                    st.rerun()

        st.divider()
        st.write(f"Catalog Items: **{len(options)}**")

    col1, col2 = st.columns(2)
    with col1:
        cust_name = st.text_input("Customer Name")
    with col2:
        cust_phone = st.text_input("Customer Phone (WhatsApp Number)")

    st.subheader("Add Item")
    if not options:
        st.warning("No products available. Please add products from the sidebar.")
    else:
        i1, i2, i3, i4 = st.columns([3, 2, 2, 1.2])
        sel_product = i1.selectbox("Product", options, key="sel_product")
        sel_price = float(price_map[sel_product])

        i2.number_input(
            "Unit Price",
            min_value=0.0,
            value=sel_price,
            step=1.0,
            format="%.2f",
            disabled=True,
            key="sel_price",
        )
        qty = int(i3.number_input("Quantity", min_value=1, max_value=999, value=1, step=1))
        i4.metric("Line Total", f"Rs {qty * sel_price:.2f}")

        st.caption(f"Selected Product Price: Rs {sel_price:.2f}")
        if st.button("Add Item", type="primary"):
            st.session_state.cart.append({
                "product": sel_product,
                "qty": qty,
                "price": sel_price,
                "total": qty * sel_price,
            })
            st.success("Item added.")

    st.subheader("Estimate Items")
    if st.session_state.cart:
        cols = st.columns([3, 1, 1.5, 1.5, 0.5])
        cols[0].write("**Product Name**")
        cols[1].write("**Quantity**")
        cols[2].write("**Unit Price**")
        cols[3].write("**Total**")
        
        for i, item in enumerate(st.session_state.cart):
            c = st.columns([3, 1, 1.5, 1.5, 0.5])
            c[0].write(item["product"])
            c[1].write(item["qty"])
            c[2].write(f"Rs {item['price']:.2f}")
            c[3].write(f"Rs {item['total']:.2f}")
            if c[4].button("🗑️", key=f"del_{i}_{item['product']}"):
                st.session_state.cart.pop(i)
                st.rerun()
                
        st.write("---")

        subtotal, total = calc_totals(st.session_state.cart)
        gst = subtotal * GST_RATE

        t1, t2, t3 = st.columns(3)
        t1.metric("Subtotal", f"Rs {subtotal:.2f}")
        t2.metric(f"GST ({int(GST_RATE*100)}%)", f"Rs {gst:.2f}")
        t3.metric("Grand Total", f"Rs {total:.2f}")

        if st.columns([1, 1])[0].button("Clear Items"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("No items added yet.")

    st.subheader("Send via WhatsApp", divider="grey")
    inv_no = st.text_input("Estimate Number", value=st.session_state.invoice_no)
    inv_date = st.date_input("Estimate Date", value=datetime.now().date()).strftime("%d-%m-%Y")

    if not st.session_state.cart:
        st.warning("Add some items to the cart above.")
    elif not cust_phone.strip():
        st.warning("Please enter a customer phone number to send the WhatsApp estimate.")
    else:
        # scrub out non-digits
        raw_phone = "".join(ch for ch in cust_phone if ch.isdigit())
        if len(raw_phone) != 10:
            st.error("Phone number must be exactly 10 digits.")
        else:
            subtotal, total = calc_totals(st.session_state.cart)
            gst = subtotal * GST_RATE
            
            link = build_wa_link(
                phone=cust_phone.strip(),
                name=cust_name.strip() or "Customer",
                inv_no=inv_no,
                inv_date=inv_date,
                items=st.session_state.cart,
                subtotal=subtotal,
                gst=gst,
                total=total,
            )
            st.link_button("Send Estimate on WhatsApp", link, type="primary")

if __name__ == "__main__":
    main()
