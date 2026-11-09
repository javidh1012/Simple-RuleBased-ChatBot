# Student Academic Assistant – Rule-Based Chatbot

🌐 **Live Demo:** [https://simple-rulebased-chatbot.onrender.com](https://simple-rulebased-chatbot.onrender.com)

A clean, modern, text-based **Student Academic Assistant** chatbot built using **Python Flask, Jinja2, Bootstrap 5, Vanilla JavaScript, and Pandas**, powered strictly by predefined Python conditional rules and a real Kaggle student performance dataset.

> 🚀 **Live Deployment:** Try the live working application on Render 👉 **[https://simple-rulebased-chatbot.onrender.com](https://simple-rulebased-chatbot.onrender.com)**
>
> **Zero External AI / LLM Models:** This application is 100% deterministic and rule-based. No Gemini, OpenAI, or external AI APIs are integrated.
>
> **Clean Modern Interface:** Clean, white/light layout with professional typography, simple rounded chat message bubbles, text input only (zero WhatsApp branding, zero voice/audio/speech recognition).

---

## 1. Application Flow & Session State Machine

The chatbot state is securely managed using **Flask Sessions** across three explicit states:

```
[START]
   │  User sends greeting (e.g., "HI", "hello", "Hey", "Good morning")
   ▼
[WAITING_FOR_STUDENT_ID]
   │  User enters Student ID (e.g., "S1000")
   ├─► Not Found ──► Responds with error message, stays in WAITING_FOR_STUDENT_ID
   ▼  Found in CSV
[VERIFIED]
   │  Displays 6 clickable menu buttons:
   │  1. My Profile
   │  2. Attendance Report
   │  3. Internal Marks
   │  4. Academic Performance
   │  5. Study Recommendations
   │  6. Logout ──► Resets session & conversation back to [START]
```

### Initial Application Load (State: `START`)
- Conversation area is **completely empty** (no initial welcome message, no menus, no student info).
- Only shows the text input field and Send button.
- The conversation begins only when the user sends a greeting.

### Greeting Recognition (Case-Insensitive via `casefold()`)
Recognizes greetings regardless of case:
- `HI`, `hi`, `Hi`
- `HELLO`, `hello`
- `Hey`, `hey`
- `Good morning`, `GOOD MORNING`
- `Good evening`, `GOOD EVENING`

**Chatbot Response:**
> *"Hello! Welcome to Student Academic Assistant! I'm here to help you understand your academic performance. To continue, please enter your Student ID."*
*(Chatbot state transitions to `WAITING_FOR_STUDENT_ID`)*

### Student Verification (State: `WAITING_FOR_STUDENT_ID`)
- Accepts the next text message as the Student ID.
- Searches for the ID in the dataset (`data/student_dataset.csv`) using Pandas.
- **If Not Found:**  
  > *"Sorry! The Student ID you entered was not found. Please check your ID and try again."*
- **If Found:**  
  > *"Student verified successfully! Welcome. How can I help you today?"*  
  Displays the 6 clickable menu buttons and sets state to `VERIFIED`.

### Verified Student Menu (State: `VERIFIED`)
1. **My Profile**: Displays student ID, attendance %, internal marks, assignment score, study hours, final marks.
2. **Attendance Report**: Evaluates attendance %, status, and personalized advice (Section 8 rules).
3. **Internal Marks**: Evaluates Internal Test 1 & 2 (out of 40), average %, and progress trend (Section 9 rules).
4. **Academic Performance**: Displays all 6 dataset metrics and overall academic standing (Section 10 rules).
5. **Study Recommendations**: Prioritized study advice based on weak and strong areas (Section 11 rules).
6. **Logout**: Clears session, resets state to `START`, and clears the conversation area back to the initial empty state.

The menu stays accessible so students can query multiple options in sequence.

---

## 2. Kaggle Dataset Grounding (All 7 Columns Confirmed)

Dataset file: `data/student_dataset.csv` (2,000 students: `S1000` to `S2999`).

| # | Column Name in CSV | Data Type | Range in Dataset | Chatbot Feature Mapping |
|---|--------------------|------|------------------|-------------------------|
| 1 | `Student_ID` | String | S1000 – S2999 | Unique Student Identifier & Flask Session Auth |
| 2 | `Attendance (%)` | Integer | 52% – 100% | Attendance Report & I-Grade Warning Rules |
| 3 | `Internal Test 1 (out of 40)` | Integer | 18 – 40 | Internal Exam Evaluation (Scale: /40) |
| 4 | `Internal Test 2 (out of 40)` | Integer | 16 – 40 | Internal Exam Evaluation & Progress Trend |
| 5 | `Assignment Score (out of 10)` | Integer | 4 – 10 | Continuous Coursework Assessment Metric |
| 6 | `Daily Study Hours` | Integer | 1 – 5 hrs/day | Independent Study Habit Evaluation |
| 7 | `Final Exam Marks (out of 100)` | Integer | 25 – 100 | End-Semester Exam Marks & Letter Grade |

---

## 3. Predefined Python Evaluation Rules

### A. Attendance Rules (Section 8)
- **> 85%**: `"Excellent! Your attendance is very good. Keep it up!"`
- **> 75% and ≤ 85%**: `"Your attendance is satisfactory (above the 75% requirement). Strive to maintain above 85% for academic honors eligibility."`
- **== 75%**: `"You are safe, but you are at the minimum attendance threshold. You must attend all upcoming classes regularly."`
- **65% to < 75%**: `"You may receive an I Grade. Attend all classes regularly and contact your class advisor regarding your attendance."`
- **< 65%**: `"You are in danger of receiving an I Grade. Contact your class advisor immediately. Submit all pending OD forms and medical certificates before I Grade processing."`

### B. Internal Examination Rules (Section 9)
Scale confirmed: out of 40.
- **30 – 40**: `"Excellent performance. Keep it up in the next internal examination."`
- **20 – 29**: `"Needs improvement. Prepare better and aim for 30+ marks."`
- **Below 20**: `"Poor performance. Study harder and aim to pass the end-semester examination."`

---

## 4. How to Run the Application

### 🌐 Live Web Demo
The application is live and deployed on Render:  
👉 **[https://simple-rulebased-chatbot.onrender.com](https://simple-rulebased-chatbot.onrender.com)**

---

### Local Installation & Run

#### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

#### Step 2: Start the Application

##### Option A: Local Development (Windows / macOS / Linux)
```powershell
python app.py
```

##### Option B: Production WSGI Deployment with Gunicorn (Linux / Docker / Render)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Step 3: Open in Browser
Navigate to:  
👉 **`http://127.0.0.1:5000`**

---

## 5. Sample Student IDs for Testing

| Student ID | Attendance (%) | Internals (/40) | Final Exam (/100) | Scenario |
|------------|----------------|-----------------|-------------------|----------|
| **`S1001`** | **91%** | 24, 33 | 56 | **Excellent Attendance (>85%)** |
| **`S1031`** | **75%** | 33, 37 | 66 | **Borderline Safe (==75%)** |
| **`S1002`** | **73%** | 29, 30 | 56 | **Attendance Warning (65%–74%)** |
| **`S1678`** | **60%** | 31, 33 | **31** | **Danger of I Grade (<65%) + Arrear Final** |
| **`S1118`** | 86% | **18**, 32 | **35** | **Poor Internal (<20) + Arrear Final (<40)** |
| **`S1000`** | 84% | 30, 36 | 72 | **Standard Good Standing Student** |

---

## 6. Automated Test Suite

To verify all greetings, state transitions, rules, and endpoints:
```powershell
python test_app.py
```

Output:
```
Testing greeting normalization with casefold()...
✅ All greeting variations recognized successfully.
Testing complete conversation state machine...
✅ Complete state machine and conversational flow passed perfectly.

🎉 ALL UNIT AND INTEGRATION TESTS PASSED WITH 100% SUCCESS!
```
