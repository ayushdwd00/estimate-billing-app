# 🧾 Billing & WhatsApp Estimate System

A sleek, dark-themed web application for creating product estimates and sending them directly to customers via WhatsApp. Built for small businesses and shops managing their product catalog and billing workflow.

![App Screenshot](screenshots/main.png)

---

## ✨ Features

- 📦 **Product Catalog Management** — Add and remove products with custom pricing
- 🛒 **Estimate Builder** — Select products, set quantities, and auto-calculate line totals
- 🧮 **Auto Tax Calculation** — Subtotal + 18% GST = Grand Total computed instantly
- 📋 **Estimate Tracking** — Auto-generated estimate numbers (e.g. `EST-20260419-204835`) with date
- 📱 **WhatsApp Integration** — Send estimates directly to customers via WhatsApp with one click
- 🗑️ **Line Item Management** — Remove individual items or clear all estimates

---

## 📸 Screenshots

| Feature | Preview |
|---|---|
| Add items & build estimate | ![Screenshot 1](screenshots/add-item.png) |
| Estimate summary with GST | ![Screenshot 2](screenshots/summary.png) |
| Send via WhatsApp | ![Screenshot 3](screenshots/whatsapp.png) |

---

## 🚀 Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Edge, Safari)
- No backend or server required — runs entirely in the browser

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/billing-whatsapp-estimate.git

# Navigate into the project
cd billing-whatsapp-estimate

# Open in browser
open index.html
```

Or simply open `index.html` directly in your browser.

---

## 🛠️ Usage

### 1. Manage Your Product Catalog
- Use the **left sidebar** to add new products with a name and price
- Delete existing products using the "Remove Product" dropdown + Delete button
- Catalog item count is shown at the bottom of the sidebar

### 2. Create an Estimate
- Enter the **Customer Name** and **WhatsApp Number**
- Select a product from the dropdown — the unit price auto-fills
- Adjust the **quantity** using the `+` / `−` controls
- Click **Add Item** to append it to the estimate
- Remove individual line items using the 🗑️ trash icon

### 3. Review Totals
| Field | Description |
|---|---|
| Subtotal | Sum of all line items |
| GST (18%) | Tax calculated on subtotal |
| Grand Total | Final amount including tax |

### 4. Send via WhatsApp
- An estimate number and date are auto-generated
- Enter or verify the customer's WhatsApp number
- Click **Send via WhatsApp** to open WhatsApp Web/App with a pre-filled message

---

## 🧩 Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | HTML / CSS / JavaScript (or React) |
| Styling | Dark theme with custom CSS |
| WhatsApp | `wa.me` deep link API |
| Storage | Browser `localStorage` for catalog persistence |

---

## 📁 Project Structure

```
billing-whatsapp-estimate/
├── index.html          # Main app entry point
├── style.css           # Dark theme styles
├── app.js              # Core logic (catalog, estimates, WhatsApp)
├── screenshots/        # App screenshots for README
└── README.md
```

---

## 🔧 Configuration

You can customize the following in `app.js`:

```js
// Tax rate (default: 18% GST)
const TAX_RATE = 0.18;

// Estimate number prefix
const ESTIMATE_PREFIX = "EST";

// WhatsApp message template
const WA_MESSAGE_TEMPLATE = `...`;
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

Made with ❤️ for small businesses.  
Questions or suggestions? Open an [issue](https://github.com/your-username/billing-whatsapp-estimate/issues).
