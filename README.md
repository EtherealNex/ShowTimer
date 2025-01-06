# Timer App for DSMs

A Python-based timer application designed for Deputy Stage Managers (DSMs) to manage and track time effectively during theatre productions. This app provides precise timing tools for Act 1, Interval, and Act 2, ensuring smooth show operations.

---

## 🎯 Features

- **Stopwatch**: Count time up from 0 with centisecond precision.
- **Countdown Timer**: Set a specific time and count down to 0.
- **Local Time Display**: Show the current system time in a simple and clear format.
- **Interval Alerts**: Automatic background color changes for critical interval warnings:
  - Amber: When 5 minutes remain.
  - Red: When the interval ends.
- **Show Insights**: Calculate and display important show time

---

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EtherealNex/ShowTimer.git

2. Navigate to the project directory
   ```bash
   cd [location of cloned repository]

3. Run the app.
   ```bash
   python main.py

---

# 🚀 How to Use:
- **SetUp**:
  - Go to app/ui
  - Change self.show_name to your show
  - Change interval times + any init settings you want

## Use
1. **Starting the Timers**:
   - Use the buttons to togle timers
   - Use the buttons to progress through the show.
2. **Viewing Show Insights**:
   - After the show you will be given a page on insights
   - Saving to JSON will save this data to a file in app/userdata/[showname].json

---

# 📁 File Structure
```css
.
├── app/
│   ├── models/
│   │   └── timer.py
│   ├── userdata/
│   │   └── info.txt
│   └── ui.py
├── README.md
├── main.py
├── .gitignore
└── LICENSE
```

- **app/**: Source code for the timer app.
- **userdata/**: Stores saved JSON files containing show timing data

---

# 🔧 Technologies Used
- **Language**: Python
- **GUI Framework**: Tkinter
- **Data Storage**: JSON files

---

# 🛠️ Future Features
- **Pre-Programmed Start Times**: Auto start actor calls as we approch the show time
- **Settings**: Creating a settings menu to alter features like timer lengths.

---

# 🧑‍💻 Contributions
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
```bash
git checkout -b feature/new-feature
```
3. Make your changes and commit them:
```bash
git commit -m "Add new feature"
```
4. Push to your fork:
```bash
git push origin feature/new-feature
```
5. Open a pull request.

---

# 📞 Contact
For questions or suggestions:
- Email: Find this on my github page
- GitHub: EtherealNex
