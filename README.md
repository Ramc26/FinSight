# 🧠 FinSight: Your Documents' AI Overlord

Ever stared at a PDF and wished it would just tell you what's important? Yeah, me too. FinSight is a tool that stops you from having to *actually* read boring documents. You upload a file, and a squad of AI agents tear it apart, figure out what's inside, and then wait for you to ask questions.

It's like having an unpaid intern who loves paperwork, never sleeps, and doesn't steal your snacks.

---

## ✨ Features That Actually Work (Most of the Time)

* **AI Agent Squad:** Powered by **CrewAI**, this isn't just one AI, it's a team. The first agent figures out *what* the document is (a ticket, an invoice, a top-secret plan), and the others extract the juicy details.
* **Chat with Your Docs:** A slick **Streamlit** UI lets you have a conversation with your PDF. Ask for a summary, find specific info, or just see if it's having a good day.
* **Password Whisperer:** Got a locked PDF? No problem. The app will politely ask for the password in the UI, not in some scary terminal window.
* **Knows Its Stuff:** It's smart enough to tell the difference between a bank statement and a train ticket, so its analysis is actually relevant.
* **Sidebar of Secrets:** See all the text and tables the agents have extracted, neatly organized in the sidebar for your viewing pleasure.

---

## 📸 A Glimpse into the Matrix

Here's what it looks like when you let the AI out of the box.

**1. The Welcome Mat:** Upload your document and let the magic begin.
![FinSight Welcome Screen](screenshots/Screenshot%202025-10-03%20at%202.44.46%E2%80%AFPM.png)

**2. Finding the Big Spenders:** Ask it to find large transactions, and it'll hunt them down and even do the math for you. Because who has time for calculators?
![FinSight analyzing large transactions](screenshots/Screenshot%202025-10-03%20at%202.44.03%E2%80%AFPM.png)

**3. Spotting Your Habits:** Curious where your money *really* goes every month? It can find all your repetitive transactions in seconds.
![FinSight finding repetitive transactions](screenshots/Screenshot%202025-10-03%20at%202.43.00%E2%80%AFPM.png)

---

## 🚀 How to Unleash the Beast

Ready to stop reading and start commanding? Here’s how you get it running.

1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/Ramc26/FinSight.git](https://github.com/Ramc26/FinSight.git)
    cd FinSight
    ```

2.  **Set Up the Environment:**
    It's always a good idea to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the Magic Spells (Dependencies):**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Give the AI Its Brain Food (API Key):**
    You'll need an OpenAI API key. Create a file named `.env` in the project root and add your key:
    ```
    OPENAI_API_KEY="your-super-secret-key-here"
    ```

5.  **Launch!**
    Run the Streamlit app from your terminal:
    ```bash
    streamlit run app.py
    ```
    Your browser should open with the app ready to go.

---

## 🛠️ The Tech Stack (What Makes the Hamster Wheel Spin)

* **Python:** The glue holding it all together.
* **Streamlit:** For the pretty face (the UI).
* **CrewAI:** For the brains of the operation (the multi-agent system).
* **PyMuPDF:** For the PDF heavy-lifting and extraction.
* **OpenAI GPT Models:** The source of all the AI magic.

Enjoy your newfound freedom from document drudgery!