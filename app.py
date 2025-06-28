

from flask import Flask, render_template, request, redirect, url_for, session, flash,Response
import matplotlib.pyplot as plt
from flask_mysqldb import MySQL
import os
import cv2
from fer import FER
import time

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'
mysql = MySQL(app)

app.secret_key = 'your-secret-key'  # Ensure this is secure for production

@app.route('/')
def home():
    return redirect(url_for('main'))  # Redirect to the main page

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/quiz')
def quiz():
    # Check if user is logged in
    if 'username' not in session:
        flash('You must be logged in to take the quiz.', 'danger')
        session['redirect_after_login'] = 'main'
        return redirect(url_for('home1'))
    
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    responses = {
        'q1': request.form.get('q1'),
        'q2': request.form.get('q2'),
        'q3': request.form.get('q3'),
        'q4': request.form.get('q4'),
        'q5': request.form.get('q5'),
        'q6': request.form.get('q6'),
        'q7': request.form.get('q7'),
        'q8': request.form.get('q8'),
        'q9': request.form.get('q9'),
        'q10': request.form.get('q10'),
        'q11': request.form.get('q11'),
        'q12': request.form.get('q12'),
        'q13': request.form.get('q13'),
        'q14': request.form.get('q14'),
        'q15': request.form.get('q15'),
        'q16': request.form.get('q16'),
        'q17': request.form.get('q17'),
        'q18': request.form.get('q18'),
        'q19': request.form.get('q19'),
        'q20': request.form.get('q20'),
    }

    # Count 'yes' responses and 'no' responses
    yes_count = sum(1 for i in range(1, 16) if responses[f'q{i}'] == 'yes')
    no_count = 15 - yes_count  # Assuming there are exactly 15 questions

    # Calculate percentage for progress bar
    progress_percentage = (yes_count / 15) * 100

    # Determine personality type based on updated conditions
    if yes_count == 8 and no_count == 7:
        personality_type = "Extrovert"
        books = [
            "How to Win Friends and Influence People by Dale Carnegie",
            "The Power of Now by Eckhart Tolle",
            "The 7 Habits of Highly Effective People by Stephen Covey",
            "Dare to Lead by Brené Brown",
            "The Art of People by Dave Kerpen"
        ]
        movies = [
            "The Social Network (2010) - A drama about the founding of Facebook.",
            "The Pursuit of Happyness (2006) - A story about resilience and determination.",
            "Crazy, Stupid, Love (2011) - A romantic comedy about love and relationships."
        ]
        insights = [
            "You thrive in social situations and enjoy being around others.",
            "You are likely to have a wide social circle.",
            "You enjoy taking risks and trying new experiences.",
            "Your energy is often infectious and uplifting.",
            "You prefer collaboration over solitary work."
        ]
    elif yes_count == 7 and no_count == 8:
        personality_type = "Introvert"
        books = [
            "The Introvert's Way: Living a Quiet Life in a Noisy World by Sophia Dembling",
            "Introvert Power: Why Your Inner Life Is Your Hidden Strength by Laurie Helgoe",
            "The Highly Sensitive Person by Elaine N. Aron"
        ]
        movies = [
            "Her (2013) - A unique love story about a man who falls in love with an operating system.",
            "A Ghost Story (2017) - A meditation on love and loss.",
            "Little Miss Sunshine (2006) - A heartwarming story of an unconventional family."
        ]
        insights = [
            "You prefer solitude and deep thinking.",
            "You often need time alone to recharge.",
            "You value close, personal relationships over large social circles."
        ]
    else:
        personality_type = "Ambivert"
        books = [
            "Quiet: The Power of Introverts in a World That Can't Stop Talking by Susan Cain",
            "Emotional Intelligence 2.0 by Travis Bradberry",
            "Atomic Habits by James Clear"
        ]
        movies = [
            "The Secret Life of Walter Mitty (2013) - A story about stepping out of one's comfort zone.",
            "The Intern (2015) - A tale of friendship across generations.",
            "Juno (2007) - A quirky story of teenage pregnancy and unexpected friendships."
        ]
        insights = [
            "You have a good balance between introversion and extroversion.",
            "You can adapt your behavior based on the situation.",
            "You enjoy social gatherings but also appreciate time alone."
        ]

    # Decision-making analysis based on the last 5 questions
    fact_based_count = 0
    emotion_based_count = 0

    # Analyze responses for decision-making
    if request.form.get('q16') == 'yes':
        fact_based_count += 1
    else:
        emotion_based_count += 1

    if request.form.get('q17') == 'yes':
        emotion_based_count += 1
    else:
        fact_based_count += 1

    if request.form.get('q18') == 'yes':
        emotion_based_count += 1
    else:
        fact_based_count += 1

    if request.form.get('q19') == 'yes':
        emotion_based_count += 1
    else:
        fact_based_count += 1

    if request.form.get('q20') == 'yes':
        fact_based_count += 1
    else:
        emotion_based_count += 1

    # Generate decision-making pie chart
    labels = ['Fact-based Decisions', 'Emotion-based Decisions']
    sizes = [fact_based_count, emotion_based_count]
    colors = ['#66b3ff', '#ff9999']

    plt.figure(figsize=(6, 3))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    chart_path = 'static/pie_chart.png'
    plt.savefig(chart_path)
    plt.close()

    # Render results page
    return render_template('result.html', 
                           yes_count=yes_count, 
                           personality_type=personality_type, 
                           insights=insights,
                           books=books,
                           movies=movies,  # Pass movies to the template
                           fact_based_count=fact_based_count,
                           emotion_based_count=emotion_based_count,
                           chart_path=chart_path,
                           progress_percentage=progress_percentage)  # Pass the progress percentage



@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/forum')
def forum():
    # Retrieve feedback from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, email, message, created_at FROM feedback ORDER BY created_at DESC")
    feedbacks = cur.fetchall()  # Get all feedback entries
    cur.close()

    return render_template('forum.html', feedbacks=feedbacks)



@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    mysql.connection.commit()
    cur.close()

    flash('Feedback submitted successfully!', 'success')
    return redirect(url_for('forum'))  # Redirect to the forum page after submitting
















































@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home1')
def home1():
    return render_template('home1.html', username=session.get('username'))  # Pass the username to the template

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM tbl_users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[1]:
            session['username'] = user[0]  # Store username in session

            # Check if there was a redirect flag set
            if session.get('redirect_after_login') == 'main':
                session.pop('redirect_after_login', None)  # Remove the flag
                return redirect(url_for('main'))  # Redirect to main.html
            return redirect(url_for('home1'))  # Redirect to home1 after successful login
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_users (username, password) VALUES (%s, %s)", (username, pwd))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))
# Initialize the video capture object
video_capture = cv2.VideoCapture(0)  # 0 is usually the default camera

# Create an instance of the FER detector
emotion_detector = FER()

@app.route('/main1')
def main1():
    return render_template('main1.html')

def generate_frames():
    last_emotion = None
    last_analysis_time = time.time()
    analysis_interval = 2  # Analyze emotions every 2 seconds

    while True:
        success, frame = video_capture.read()  # Read a frame from the webcam
        if not success:
            break
        else:
            # Check if it's time to analyze the frame
            current_time = time.time()
            if current_time - last_analysis_time >= analysis_interval:
                # Detect emotions in the frame
                emotions = emotion_detector.detect_emotions(frame)

                # If any emotions were detected, get the dominant emotion
                if emotions:
                    dominant_emotion = emotions[0]['emotions']
                    last_emotion = max(dominant_emotion, key=dominant_emotion.get)  # Get the emotion with the highest score
                
                # Update the last analysis time
                last_analysis_time = current_time

            # Display the last detected emotion
            if last_emotion is not None:
                cv2.putText(frame, f'Emotion: {last_emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame to be sent to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
